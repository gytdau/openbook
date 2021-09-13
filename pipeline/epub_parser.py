from bs4.element import Comment, NavigableString
from content_parser import Navpoint, ContentParser
import sys
import os
import hashlib

from zipfile import ZipFile
from zipfile import is_zipfile
from titlecase import titlecase

from slugify import slugify
from bs4 import BeautifulSoup

import random
from helpers import join_path
import helpers


class EpubParser(object):
    def __init__(self, filename, file = None):
        self.file = file
        self.filename = filename
        self.html_file_order = []
        self.html_files = {}
        self.image_files = {}
        self.navpoints = {}
        self.ezip = None
        self.file_hash = None
        self.parse()

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

        if(self.file):
            data = self.file.read()
            self.file_hash = hashlib.sha256(data).hexdigest()
            self.file.seek(0)
            self.ezip = ZipFile(self.file, 'r')
        else:
            with open(self.filename,"rb") as f:
                data = f.read()
                self.file_hash = hashlib.sha256(data).hexdigest()
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

        self.populate_html_page_list(content, content_directory_path)
        self.populate_image_list(content, content_directory_path)

        self.process_navpoints(ncx)

        self.content = ContentParser(self.html_file_order, self.html_files, self.image_files,
                                     self.navpoints)

        return self

    def set_metadata_from_xml(self, content: BeautifulSoup):
        self.title = self._try_get_text(content, "dc:title")
        self.description = self._try_get_text(content, "dc:description")
        self.author = self._try_get_text(content, "dc:creator")
        self.slug = f'{slugify(self.title)}_{random.randint(0, 1000)}'

    def process_navpoints(self, ncx: BeautifulSoup):
        navpoints = ncx.find_all("navpoint")

        # sort them by playorder
        navpoints = sorted(
            navpoints, key=lambda elem: int(elem.attrs["playorder"]))

        for navpoint in navpoints:
            navpoint: BeautifulSoup

            title = navpoint.find("text").text
            filename, selector = self._normalize_navlink_src(
                navpoint.find("content").attrs["src"])

            navpoint_to_add = Navpoint(title=title, selector=selector)

            if filename in self.navpoints:
                self.navpoints[filename].append(
                    navpoint_to_add)
            else:
                self.navpoints[filename] = [navpoint_to_add]

        self.add_navpoint_to_start_of_book()

    def add_navpoint_to_start_of_book(self):
        first_html_page = self.html_file_order[0]
        new_navpoint = Navpoint(title=self.title, selector=None)

        if first_html_page in self.navpoints:
            # self.navpoints[first_html_page].append(new_navpoint
            #     )
            pass
            # Just to see if this actually mattered before
        else:
            self.navpoints[first_html_page] = [new_navpoint]

    def can_be_unzipped(self):
        return not self.ezip.testzip()

    def get_file_content(self, filename):
        data = None
        if filename.startswith("/"):
            filename = filename[1:]
        with self.ezip.open(filename) as f:
            data = f.read()
        return data

    def get_file_content_xml(self, filename):
        if filename.startswith("/"):
            filename = filename[1:]
        with self.ezip.open(filename) as f:
            return BeautifulSoup(f, features="lxml")

    def populate_html_page_list(self, content: BeautifulSoup, content_directory_path):
        spine_tag = content.find('spine')
        for spine_item_tag in spine_tag.children:
            spine_item_tag: BeautifulSoup
            if type(spine_item_tag) == NavigableString:
                continue

            idref = spine_item_tag.attrs['idref']
            # Dots are valid in IDs, but they must be escaped for us to use them in a selector
            idref = idref.replace(".", "\.")
            corresponding_item = content.select_one(f"#{idref}")
            filename = corresponding_item.attrs['href']

            if filename in self.html_file_order:
                continue

            file_content = self.get_file_content_xml(
                join_path(content_directory_path, filename))

            self.html_files[filename] = file_content
            self.html_file_order.append(filename)

    def populate_image_list(self, content: BeautifulSoup, content_directory_path):
        manifest_tag = content.find('manifest')
        for manifest_item_tag in manifest_tag.children:
            manifest_item_tag: BeautifulSoup
            if type(manifest_item_tag) == NavigableString or type(manifest_item_tag) == Comment:
                continue

            mimetype: str = manifest_item_tag.attrs['media-type']

            if not mimetype.startswith("image/"):
                continue

            filename = manifest_item_tag.attrs['href']
            file_content = self.get_file_content(
                join_path(content_directory_path, filename))

            self.image_files[filename] = file_content

    def __str__(self):
        return f"`{self.title}` -> `{self.slug}`"


if __name__ == '__main__':
    # For use in the debugger.
    # filename = "/home/gytis/Projects/openbook/pipeline/epubs/oscar-wilde_the-picture-of-dorian-gray.epub"
    # filename = "/home/gytis/Projects/openbook/pipeline/epubs/pg66080-images.epub"
    filename = "/media/gytdau/Filestore/Projects/openbook/pipeline/epubs/private/The Fabric of Reality - David Deutsch.epub"
    epub = EpubParser(filename)

    url = helpers.parse_s3_url("s3://gutenberg-vivlia/pg1-images.epub")
    epub = helpers.EpubParserFromS3(**url)
