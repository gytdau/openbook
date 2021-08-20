import os

from zipfile import ZipFile
from zipfile import is_zipfile

from slugify import slugify
from bs4 import BeautifulSoup

import random


class EPUB(object):

    @staticmethod
    def _join_path(path, filename):
        """
        epub path are unix based, we require this method for this to work correctly on windows
        """
        return '/'.join([path, filename])

    def _process_chapter(self, chapter: BeautifulSoup):
        body = chapter.find("body")
        body.name = "div"
        body = str(body)
        return body

    def _normalize_navlink_src(self, filename):
        if "#" in filename:
            # A selector is at the end. Remove it. TODO: Figure out why?
            filename = filename.split("#")[0]
        return filename

    def __init__(self, filename):
        print(f"Processing: {filename}")

        self.ezip = ZipFile(filename, 'r')
        if(not self.is_valid()):
            return

        container = self.get_file_content_xml("META-INF/container.xml")
        content_path = container.find("rootfile").attrs["full-path"]
        content_directory_path = os.path.dirname(content_path)
        content = self.get_file_content_xml(content_path)

        self.title = content.find("dc:title").text
        description_element = content.find("dc:description")
        self.description = description_element.text if description_element else ""
        self.author = content.find("dc:creator").text
        self.slug = f'{slugify(self.title)}_{random.randint(0, 1000)}'

        print(f"Reading: {self}")

        ncx = self.get_file_content_xml(self._join_path(content_directory_path, content.select_one("#ncx").attrs["href"]))

        self.chapters = []

        for navpoint in ncx.find_all("navpoint"):
            navpoint: BeautifulSoup

            chapter_title = navpoint.find("text").text
            chapter_path = self._normalize_navlink_src(navpoint.find("content").attrs["src"])
            chapter = self.get_file_content_xml(self._join_path(content_directory_path, chapter_path))

            print(f"\t- Processing Chapter: {chapter_title}")

            chapter_content = self._process_chapter(chapter)

            self.chapters.append((
                int(navpoint['playorder']),
                chapter_title,
                chapter_path,
                chapter_content
            ))
        self.chapters.sort()

    def is_valid(self):
        return self.ezip.testzip()

    def list_files(self):
        return self.ezip.namelist()

    def get_file_content(self, filename):
        data = None
        with self.ezip.open(filename) as f:
            data = f.read()
        return data

    def get_file_content_xml(self, filename):
        with self.ezip.open(filename) as f:
            return BeautifulSoup(f, features="lxml")

    def get_chapters(self):
        return self.chapters

    def __str__(self):
        a = [self.title, self.slug, self.author, self.description]
        a = [x for x in a if x]
        return " - ".join(a)



import sys
if __name__ == '__main__':
    filename = sys.argv[1]
    epub = EPUB(filename)
