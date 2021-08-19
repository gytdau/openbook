import sys
import json
import os
from bs4 import BeautifulSoup
import shutil
from slugify import slugify
import sqlite3
import random


def normalize_navlink_src(filename):
    if "#" in filename:
        # A selector is at the end. Remove it. TODO: Figure out why?
        filename = filename.split("#")[0]
    return filename


def process_chapter(chapter: BeautifulSoup, filename, slug, output):
    body = chapter.find("body")
    body.name = "div"
    body = str(body)
    result_path = f'{output}/{slug}/{filename}'
    with open(result_path, "w") as f:
        f.write(body)
    return result_path


def process_epub(filename, output):
    filename_without_extension = filename.split(".")[0]

    shutil.unpack_archive(filename, filename_without_extension, "zip")

    def get_file(filename, relative_to=None):

        if relative_to:
            relative_to = os.path.dirname(relative_to)
            filename = os.path.join(relative_to, filename)

        with open(f'{filename_without_extension}/{filename}') as f:
            return (BeautifulSoup(f, features="lxml"), filename)

    container, _ = get_file("META-INF/container.xml")
    content, content_path = get_file(
        container.find("rootfile").attrs["full-path"])

    title = content.find("dc:title").text
    description_element = content.find("dc:description")
    description = description_element.text if description_element else ""
    author = content.find("dc:creator").text

    slug = f'{slugify(title)}_{random.randint(0, 1000)}'
    os.makedirs(f'{output}/{slug}', exist_ok=True)

    ncx, ncx_path = get_file(content.select_one(
        "#ncx").attrs["href"], content_path)
    # print(ncx)
    chapters = []

    for navpoint in ncx.find_all("navpoint"):
        # Todo: sort by playorder attribute of navpoints.
        navpoint: BeautifulSoup
        # print(navpoint)
        chapter_title = navpoint.find("text").text
        chapter_path = normalize_navlink_src(
            navpoint.find("content").attrs["src"])
        chapter, _ = get_file(
            chapter_path, content_path)

        result_path = process_chapter(chapter, chapter_path, slug, output)

        chapters.append((
            chapter_title,
            result_path,
        ))

    shutil.rmtree(filename_without_extension)
    return ((
        title,
        author,
        slug,
        description,
    ), chapters)


def create_tables(con: sqlite3.Connection):
    cur = con.cursor()
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
    con.commit()


def add_book(book, con: sqlite3.Connection):
    cur = con.cursor()
    cur.execute(
        '''INSERT INTO books (title, author, slug, description) VALUES (?, ?, ?, ?)''', book)
    con.commit()
    return cur.lastrowid


def add_chapters(book_id, chapters, con: sqlite3.Connection):
    cur = con.cursor()
    for chapter in chapters:
        cur.execute(
            '''INSERT INTO chapters (book_id, title, location) VALUES (?, ?, ?)''', (book_id, chapter[0], chapter[1]))
    con.commit()


def process_epubs(filenames, con: sqlite3.Connection, output):
    os.makedirs("output", exist_ok=True)
    create_tables(con)

    for filename in filenames:
        book, chapters = process_epub(filename, output)
        book_id = add_book(book, con)
        add_chapters(book_id, chapters, con)
