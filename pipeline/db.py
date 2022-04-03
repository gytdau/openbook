import psycopg2


class db(object):

    def __init__(self, dsn, create_tables=True, version_marker=1):
        # dsn = "user={} password={} host={} port={} dbname={} sslmode=require"
        self.dsn = dsn
        self._con = None
        if create_tables:
            self._create_tables()
        self.version = version_marker

    @property
    def con(self):
        if self._con is not None:
            return self._con
        self._con = psycopg2.connect(self.dsn)
        return self._con

    def _create_tables(self):
        cur = self.con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS ebook_source (
            id SERIAL PRIMARY KEY,
            source text,
            source_id text,
            s3_path text,
            hash_sha256 text,
            UNIQUE(hash_sha256)
        )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS books (
                id SERIAL PRIMARY KEY,
                ebook_source_id integer NOT NULL,
                title text NOT NULL,
                author text,
                slug text,
                version integer NOT NULL,
                description text,
                publication DATE,
                FOREIGN KEY (ebook_source_id) REFERENCES ebook_source (id)
            )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS chapters (
            id SERIAL PRIMARY KEY,
            book_id integer NOT NULL,
            title text,
            slug text,
            content text,
            content_stripped text,
            chapter_order integer,
            version integer NOT NULL,
            searchable_tsvector tsvector,
            FOREIGN KEY (book_id) REFERENCES books (id),
            CONSTRAINT unique_chapter_version UNIQUE(book_id, slug, chapter_order, version)
        )''')
        cur.execute('''CREATE INDEX IF NOT EXIST searchable_idx
            ON chapters USING GIN (searchable_tsvector);''')
        cur.execute('''CREATE TABLE IF NOT EXISTS paragraphs (
            id SERIAL PRIMARY KEY,
            chapters_id integer NOT NULL,
            paragraph_order integer NOT NULL,
            content text,
            colour text,
            version integer NOT NULL,
            FOREIGN KEY (chapters_id) REFERENCES chapters (id),
            CONSTRAINT unique_chapter_version_tbl_paragraphs UNIQUE(chapters_id, paragraph_order, version)
        )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS images (
            id SERIAL PRIMARY KEY,
            book_id integer NOT NULL,
            location text,
            content bytea,
            format text,
            hint text,
            version integer NOT NULL,
            FOREIGN KEY (book_id) REFERENCES books (id),
            CONSTRAINT unique_image_version UNIQUE(book_id, location, version)
        )''')
        cur.execute('''CREATE OR REPLACE LANGUAGE plv8;''')
        cur.execute('''CREATE OR REPLACE FUNCTION unescape_html(html text) RETURNS text AS $$
            var entityPattern = /&([a-z]+);/ig;
            const entities = {
                'amp': '&',
                'apos': "'",
                'lt': '<',
                'gt': '>',
                'quot': '"',
                'nbsp': '\xa0'
            };
            return html.replace(entityPattern,
                function(match, entity)
                {
                    entity = entity.toLowerCase();
                    if(entities.hasOwnProperty(entity))
                    {
                        return entities[entity];
                    }
                    else if(entity.startsWith('#'))
                    {
                        return String.fromCharCode(entity.substr(1))
                    }
                    return match;
                }
            )
        $$ LANGUAGE plv8;''')

        cur.execute('''CREATE OR REPLACE LANGUAGE plpgsql;''')
        cur.execute('''CREATE OR REPLACE FUNCTION html_strip(html text) RETURNS text AS $$
                BEGIN
                        RETURN  unescape_html(REGEXP_REPLACE(array_to_string(xpath('//text()', xmlparse(document html)), ' '), '\s+', ' ', 'g'));
                END;
        $$ LANGUAGE plpgsql;''')
        cur.execute('''CREATE OR REPLACE FUNCTION html_to_paragraph(html text) RETURNS text[] AS $$
                BEGIN
                    RETURN string_to_array(
                        REGEXP_REPLACE(
                            array_to_string(
                                xpath('//p[text()][normalize-space()]', xmlparse(document html)
                                    ), '0x13374141'
                            ), '\s+', ' ', 'g'
                        ), '0x13374141'
                    );
                END;
        $$ LANGUAGE plpgsql;''')
        cur.execute('''CREATE OR REPLACE FUNCTION prepare_chapter_search()
        RETURNS trigger AS $$
        BEGIN
            NEW.content_stripped = html_strip(NEW.content);
            NEW.searchable_tsvector = to_tsvector('english', (select string_agg(txt, ' ') from unnest(string_to_array(coalesce(NEW.content_stripped,''), ' ')) with ordinality as tmp(txt) where length(txt) < 20))
        RETURN NEW;
        END$$ LANGUAGE 'plpgsql';''')

        cur.execute('''CREATE OR REPLACE FUNCTION create_paragraphs()
        RETURNS trigger AS '
        BEGIN
            INSERT INTO paragraphs (chapters_id, paragraph_order, content, version)
                SELECT NEW.id, paragraph_order, a.content, 1 FROM unnest(html_to_paragraph(NEW.content)) WITH ORDINALITY AS a(content, paragraph_order) ON CONFLICT DO NOTHING;
            RETURN NEW;
        END' LANGUAGE 'plpgsql';''')
        cur.execute(
            '''DROP TRIGGER IF EXISTS trigger_create_paragraphs on chapters;''')
        cur.execute('''CREATE TRIGGER trigger_create_paragraphs AFTER INSERT or UPDATE ON chapters FOR EACH ROW
        EXECUTE PROCEDURE create_paragraphs();''')

        cur.execute(
            '''DROP TRIGGER IF EXISTS strip_chapter_html on chapters;''')
        cur.execute(
            '''DROP TRIGGER IF EXISTS prepare_chapter_search on chapters;''')
        cur.execute('''CREATE TRIGGER prepare_chapter_search BEFORE INSERT or UPDATE ON chapters FOR EACH ROW
        EXECUTE PROCEDURE prepare_chapter_search();''')
        cur.execute('''CREATE INDEX IF NOT EXIST idx 
            ON books USING gist ( 
            (
                to_tsvector('english', coalesce(title, '')) || 
                to_tsvector('english', coalesce(author, ''))
            ) 
        ) ;''')

        self.con.commit()

    def drop_tables(self):
        cur = self.con.cursor()
        for table_name in ['images', 'chapters', 'books', 'ebook_source']:
            cur.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE;")
        self.con.commit()

    def get_book_by_ebook_source_id(self, ebook_source_id):
        cur = self.con.cursor()
        cur.execute(
            '''SELECT * FROM books WHERE ebook_source_id = %s;''', (ebook_source_id,))
        return cur.fetchone()

    def get_books_count(self):
        cur = self.con.cursor()
        cur.execute(
            '''SELECT count(*) FROM books;''')
        return cur.fetchone()[0]

    def add_book(self, ebook_source_id, title, author, slug, description, publication):
        cur = self.con.cursor()
        cur.execute(
            '''INSERT INTO books (ebook_source_id, title, author, slug, description, version, publication) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id''',
            (ebook_source_id, title, author, slug, description, self.version, publication))
        self.con.commit()
        return cur.fetchone()[0]

    def get_all_book_source(self):
        cur = self.con.cursor()
        cur.execute(
            '''SELECT * FROM ebook_source;''')
        return cur.fetchall()

    def get_book_source_by_hash(self, hash_sha256):
        cur = self.con.cursor()
        cur.execute(
            '''SELECT * FROM ebook_source WHERE hash_sha256 = %s;''', (hash_sha256,))
        return cur.fetchone()

    def get_book_source_by_id(self, ebook_source_id):
        cur = self.con.cursor()
        cur.execute(
            '''SELECT * FROM ebook_source WHERE id = %s;''', (ebook_source_id,))
        return cur.fetchone()

    def add_book_source(self, source, source_id, s3_path, hash_sha256):
        cur = self.con.cursor()
        cur.execute(
            '''INSERT INTO ebook_source (source, source_id, s3_path, hash_sha256) VALUES (%s, %s, %s, %s) RETURNING id''', (source, source_id, s3_path, hash_sha256))
        self.con.commit()
        return cur.fetchone()[0]

    def add_chapters(self, book_id, chapters):
        cur = self.con.cursor()
        for chapter in chapters:
            cur.execute(
                '''INSERT INTO chapters (book_id, title, slug, content, chapter_order, version) VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT ON CONSTRAINT unique_chapter_version DO NOTHING;''',
                (book_id, chapter.title, chapter.slug, chapter.content, chapter.order, self.version))
        self.con.commit()

    def add_images(self, book_id, images):
        cur = self.con.cursor()
        for image in images:
            cur.execute(
                '''INSERT INTO images (book_id, location, content, format, version) VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT ON CONSTRAINT unique_image_version DO NOTHING;''',
                (book_id, image.location, image.content(), image.format, self.version))
        self.con.commit()

    def get_featured_books(self):
        cur = self.con.cursor()
        source_ids = [1342, 1232, 1727, 2554, 3207, 20203, 996, 41, 766, 3296, 1399, 2680, 779,
                      16643, 1250, 36, 35, 29720, 21279, 6130, 1727, 3296, 1974, 7700, 3296, 131, 398, 1653, 1549]
        source_ids = [f"\'pg{x}-images.epub\'" for x in source_ids]
        cur.execute(
            f'''SELECT books.title, books.author,
       LEFT(chapters.content_stripped, 500) AS sample
             FROM
            ebook_source
          JOIN books ON books.ebook_source_id = ebook_source.id
       LEFT JOIN chapters
              ON books.id = chapters.book_id
           WHERE
          ebook_source.source_id IN ({", ".join(source_ids)})
          AND
                  chapters.chapter_order = 4;''')
        return cur.fetchall()


    def get_featured_books_paragraphs(self):
        cur = self.con.cursor()
        source_ids = [1342, 1232, 1727, 2554, 3207, 20203, 996, 41, 766, 3296, 1399, 2680, 779,
                      16643, 1250, 36, 35, 29720, 21279, 6130, 1727, 3296, 1974, 7700, 3296, 131, 398, 1653, 1549]
        cur.execute(
            f'''SELECT id, regexp_replace(content_stripped, E'[\\n\\r\\u2028]+', ' ', 'g' ) as content_stripped FROM (
                    SELECT id, html_strip(content) as content_stripped FROM paragraphs WHERE chapters_id IN (
                        SELECT id FROM chapters WHERE book_id IN (
                            SELECT id FROM books WHERE ebook_source_id IN (
                                select id FROM (
                                    SELECT id, CAST(unnest(regexp_matches(source_id, 'pg(\d+)-images\.epub', 'g')) as integer) AS epub_books_id FROM public.ebook_source
                                ) source_id
                                WHERE epub_books_id IN ({", ".join([str(i) for i in source_ids])})
                            )
                        )
                    )
                ) tmp WHERE length(content_stripped) > 50 limit 10
            ''')
        return cur.fetchall()

    def update_paragraphs_colour(self, id, colour):
        cur = self.con.cursor()
        cur.execute('UPDATE paragraphs SET colour=%s WHERE id = %s', (colour, id,))
        return cur.fetchall()

    def close(self):
        self.con.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print("DB Exited")
        self.close()

if __name__ == "__main__":
    from config import config
    db_connection = config["DB_CONNECTION"]
    con = db(db_connection)
    del con
