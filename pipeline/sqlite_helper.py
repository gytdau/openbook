import sqlite3

class sqlite_helper(object):

    def __init__(self, filename):
        self.con = sqlite3.connect(filename)
        self._create_tables()


    def _create_tables(self):
        cur = self.con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS books (
                id integer PRIMARY KEY,
                title text NOT NULL,
                author text,
                slug text,
                description text
            )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS chapters (
            id integer PRIMARY KEY,
            book_id integer NOT NULL,
            title text,
            location text,
            FOREIGN KEY (book_id) REFERENCES books (id)
        )''')
        self.con.commit()


    def add_book(self, book):
        cur = self.con.cursor()
        cur.execute(
            '''INSERT INTO books (title, author, slug, description) VALUES (?, ?, ?, ?)''', book)
        self.con.commit()
        return cur.lastrowid


    def add_chapters(self, book_id, chapters):
        cur = self.con.cursor()
        for title, location in chapters:
            cur.execute(
                '''INSERT INTO chapters (book_id, title, location) VALUES (?, ?, ?)''', (book_id, title, location))
        self.con.commit()
