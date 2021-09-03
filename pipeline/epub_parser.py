from bs4.element import NavigableString
from page_parser import Navpoint, PageParser
import sys
import os

from zipfile import ZipFile
from zipfile import is_zipfile
from titlecase import titlecase

from slugify import slugify
from bs4 import BeautifulSoup

import random
from helpers import join_path


class EpubParser(object):
    def __init__(self, filename):
        self.filename = filename
        self.file_order = []
        self.files = {}
        self.navpoints = {}
        self.chapters = None
        self.ezip = None

    @staticmethod
    def _try_get_text(content, selector):
        elem = content.find(selector)
        if elem and elem.text:
            return elem.text
        return ""

    def _normalize_navlink_src(self, filename):
        if "#" in filename:
            return filename.split("#")
        return (filename, None)

    def parse(self):
        print(f"Processing: {self.filename}")

        self.ezip = ZipFile(self.filename, 'r')
        if not self.can_be_unzipped():
            return

        container = self.get_file_content_xml("META-INF/container.xml")
        content_path = container.find("rootfile").attrs["full-path"]
        content_directory_path = os.path.dirname(content_path)
        content = self.get_file_content_xml(content_path)

        self.set_metadata_from_xml(content)

        print(f"Reading: {self}")

        ncx = self.get_file_content_xml(
            join_path(content_directory_path, content.select_one("#ncx").attrs["href"]))

        self.populate_self_from_spine(content, content_directory_path)

        self.process_navpoints(ncx)

        print(PageParser(self.file_order, self.files,
                         self.navpoints).parse_into_pages())

        return self

    def set_metadata_from_xml(self, content: BeautifulSoup):
        self.title = self._try_get_text(content, "dc:title")
        self.description = self._try_get_text(content, "dc:description")
        self.author = self._try_get_text(content, "dc:creator")
        self.slug = f'{slugify(self.title)}_{random.randint(0, 1000)}'

    def process_navpoints(self, ncx: BeautifulSoup):
        self.chapters = []
        navpoints = ncx.find_all("navpoint")

        # sort them by playorder
        navpoints = sorted(
            navpoints, key=lambda elem: int(elem.attrs["playorder"]))

        for navpoint in navpoints:
            navpoint: BeautifulSoup

            title = navpoint.find("text").text
            title = titlecase(title)
            filename, selector = self._normalize_navlink_src(
                navpoint.find("content").attrs["src"])

            navpoint_to_add = Navpoint(title=title, selector=selector)

            if filename in self.navpoints:
                self.navpoints[filename].append(
                    navpoint_to_add)
            else:
                self.navpoints[filename] = [navpoint_to_add]

    def can_be_unzipped(self):
        return not self.ezip.testzip()

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

    def populate_self_from_spine(self, content: BeautifulSoup, content_directory_path):
        spine_tag = content.find('spine')
        for spine_item_tag in spine_tag.children:
            spine_item_tag: BeautifulSoup
            if type(spine_item_tag) == NavigableString:
                continue

            idref = spine_item_tag.attrs['idref']
            corresponding_item = content.select_one(f"#{idref}")
            filename = corresponding_item.attrs['href']

            file_content = self.get_file_content_xml(
                join_path(content_directory_path, filename))

            self.files[filename] = file_content
            self.file_order.append(filename)

    def __str__(self):
        a = [self.title, self.slug, self.author, self.description]
        a = [x for x in a if x]
        return " - ".join(a)


if __name__ == '__main__':
    filename = sys.argv[1]
    epub = EpubParser(filename).parse()
