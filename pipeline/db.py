import psycopg2

from helpers import join_path


class db(object):

    def __init__(self, dsn, create_tables=True, version_marker=1):
        # dsn = "user={} password={} host={} port={} dbname={} sslmode=require"
        self.con = psycopg2.connect(dsn)
        if create_tables:
            self._create_tables()
        self.version = version_marker

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
            FOREIGN KEY (book_id) REFERENCES books (id),
            CONSTRAINT unique_chapter_version UNIQUE(book_id, slug, chapter_order, version)
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

    def add_book(self, ebook_source_id, title, author, slug, description, publication):
        cur = self.con.cursor()
        cur.execute(
            '''INSERT INTO books (ebook_source_id, title, author, slug, description, version, publication) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id''',
            (ebook_source_id, title, author, slug, description, self.version, publication))
        self.con.commit()
        return cur.fetchone()[0]

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
                '''INSERT INTO chapters (book_id, title, slug, content, content_stripped, chapter_order, version) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT ON CONSTRAINT unique_chapter_version DO NOTHING;''',
                (book_id, chapter.title, chapter.slug, chapter.content, chapter.content_stripped, chapter.order, self.version))
        self.con.commit()

    def add_images(self, book_id, images):
        cur = self.con.cursor()
        for image in images:
            cur.execute(
                '''INSERT INTO images (book_id, location, content, format, version) VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT ON CONSTRAINT unique_image_version DO NOTHING;''',
                (book_id, image.location, image.content, image.format, self.version))
        self.con.commit()
