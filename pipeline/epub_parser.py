from bs4.element import Comment, NavigableString
from content_parser import Navpoint, ContentParser
import os
import hashlib

from zipfile import ZipFile
from zipfile import is_zipfile
from titlecase import titlecase

from slugify import slugify
from bs4 import BeautifulSoup

import random
from helpers import join_path


class EpubParser(object):
    def __init__(self, filename, file=None):
        self.file = file
        self.filename = filename
        self.html_file_order = []
        self.html_files = {}
        self.image_files = {}
        self.navpoints = {}
        self.ezip = None
        self.file_hash = None
        if(self.file):
            self.file_hash = self._calc_sha256(self.file)
            self.file.seek(0)
            self.ezip = ZipFile(self.file, 'r')
        else:
            with open(self.filename, "rb") as f:
                self.file_hash = self._calc_sha256(f)
            self.ezip = ZipFile(self.filename, 'r')

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

    def _calc_sha256(self, f):
        sha256 = hashlib.sha256()
        while True:
            data = f.read(sha256.block_size)
            if not data:
                break
            sha256.update(data)
        return sha256.hexdigest()

    def parse(self):
        """Main function which parses the EPUB file and populates the class attributes with the resulting data.

        Returns:
            EpubParser -- The current instance of the class"""

        print(f"Processing: {self.filename}")

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
        """Sets the metadata from the EPUB's container.xml file.

        Arguments:
            content {BeautifulSoup} -- The BeautifulSoup representation of the container.xml file.

        Returns:
            None
        """

        self.title = self._try_get_text(content, "dc:title")
        self.description = self._try_get_text(content, "dc:description")
        self.author = self._try_get_text(content, "dc:creator")
        self.publication = self._try_get_text(content, "dc:date")
        self.slug = f'{slugify(self.title)}_{random.randint(0, 1000)}'

    def process_navpoints(self, ncx: BeautifulSoup):
        """Processes the navpoints in the EPUB's NCX file.

        Arguments:
            ncx {BeautifulSoup} -- The BeautifulSoup representation of the NCX file.

        Returns:
            None
        """
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
        """Adds a navpoint to the start of the book. This is used in case the book doesn't have a navpoint in the
        beginning of the book.

        Returns:
            None
        """
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
        """Checks if the EPUB file can be unzipped. Correctly formatted EPUB files should be able to be unzipped.

        Returns:
            bool -- True if the EPUB file can be unzipped, False otherwise.
        """
        return not self.ezip.testzip()

    def get_file_content(self, filename):
        """Gets the content of a file in the EPUB file.

        Arguments:
            filename {str} -- The name of the file to get the content of.

        Returns:
            bytes -- The content of the file.
        """
        data = None
        if filename.startswith("/"):
            filename = filename[1:]
        with self.ezip.open(filename) as f:
            data = f.read()
        return data

    def get_file_content_xml(self, filename):
        """Gets the content of a file in the EPUB file and parses it as XML.

        Arguments:
            filename {str} -- The name of the file to get the content of.

        Returns:
            BeautifulSoup -- The BeautifulSoup representation of the file's content.
        """
        if filename.startswith("/"):
            filename = filename[1:]
        with self.ezip.open(filename) as f:
            return BeautifulSoup(f, features="lxml")

    def populate_html_page_list(self, content: BeautifulSoup, content_directory_path):
        """Populates the html_file_order and html_files attributes with the content of the EPUB's HTML files. The
        html_file_order attribute is a list of the filenames of the HTML files in the order they appear in the EPUB.
        The html_files attribute is a dictionary of the filenames of the HTML files and their BeautifulSoup
        representations.

        Arguments:
            content {BeautifulSoup} -- The BeautifulSoup representation of the container.xml file.
            content_directory_path {str} -- The path to the directory which contains the EPUB's content.

        Returns:
            None
        """
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

            full_path = join_path(content_directory_path, filename)
            def file_content(
                full_path=full_path): return self.get_file_content_xml(full_path)

            self.html_files[filename] = file_content
            self.html_file_order.append(filename)

    def populate_image_list(self, content: BeautifulSoup, content_directory_path):
        """Populates the image_files attribute with the content of the EPUB's images. The image_files attribute is a
        dictionary of the filenames of the images and the bytes of the images.

        Arguments:
            content {BeautifulSoup} -- The BeautifulSoup representation of the container.xml file.
            content_directory_path {str} -- The path to the directory which contains the EPUB's content.

        Returns:
            None"""
        manifest_tag = content.find('manifest')
        for manifest_item_tag in manifest_tag.children:
            manifest_item_tag: BeautifulSoup
            if type(manifest_item_tag) == NavigableString or type(manifest_item_tag) == Comment:
                continue

            mimetype: str = manifest_item_tag.attrs['media-type']

            if not mimetype.startswith("image/"):
                continue

            filename = manifest_item_tag.attrs['href']
            full_path = join_path(content_directory_path, filename)
            def file_content(
                full_path=full_path): return self.get_file_content(full_path)

            self.image_files[filename] = file_content

    def __str__(self):
        return f"`{self.title}` -> `{self.slug}`"


if __name__ == '__main__':
    # For use in the debugger.
    # filename = "/home/gytis/Projects/openbook/pipeline/epubs/oscar-wilde_the-picture-of-dorian-gray.epub"
    # filename = "/home/gytis/Projects/openbook/pipeline/epubs/pg66080-images.epub"
    filename = '/media/gytdau/Filestore/Projects/openbook/Don Quixote - Miguel De Cervantes Saavedra.epub'
    epub = EpubParser(filename)

    # url = helpers.parse_s3_url("s3://gutenberg-vivlia/pg1-images.epub")
    # epub = helpers.EpubParserFromS3(**url)
