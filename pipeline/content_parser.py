import typing
import uuid
import re
from bs4 import BeautifulSoup
from slugify import slugify
from typing import ByteString, List, Dict, NamedTuple, Tuple
import copy
from dataclasses import dataclass

from titlecase import titlecase
import bs4


@dataclass
class Navpoint:
    title: str
    selector: str


@dataclass
class Chapter:
    title: str
    slug: str
    content: str
    order: int


@dataclass
class RawChapter:
    title: str
    content: BeautifulSoup
    order: int = None


@dataclass
class Image:
    location: str
    content: ByteString
    format: str


def title_to_slug(title):
    return slugify(title)


def latin_numerals(word, **kwargs):
    if all(c in 'LXIV.' for c in word.upper()):
        # It's a Latin numeral
        return word.upper()


def titlecase_chapter(title):
    return titlecase(title, callback=latin_numerals)


def content_into_stripped_text(content):
    text = content.text
    rex = re.compile(r'\s+')
    return rex.sub(' ', text)


class ContentParser(object):
    def __init__(self, file_order: List[str], html_files: Dict[str, BeautifulSoup], image_files: Dict[str, typing.Any], navpoints: Dict[str, List[Navpoint]]):
        # file_order: [file_id, ...]
        # File order is derived from the spine of content.opf

        # files: { file_id: BeautifulSoup_page }
        # Contains the HTML files as BS4 classes

        # navpoints: { file_id: [{title, selector}, {title, selector}, ...] }
        # Navpoints are sorted into their files in this dictionary. Each navpoint is represented as a named tuple
        # navpoint.selector can be None to mean it begins at the top of the page

        # Input
        self.file_order = file_order
        self.html_files = html_files
        self.image_files = image_files
        self.navpoints = navpoints

        # Output
        self.chapters = []
        self.images = []

        # Helpers
        self.chapter_carry_over = None
        self.current_order = 0
        self.location_mapping = {}
        self.raw_chapters = []

        self.allocate_locations()
        self.parse_chapters()
        self.swap_locations_in_parsed_chapters()

        self.chapter_carry_over = None
        self.location_mapping = None
        self.file_order = None
        self.html_files = None
        self.image_files = None
        self.navpoints = None
        self.convert_raws_to_output()

    def allocate_locations(self):
        # for index, html_file in enumerate(self.file_order):
        #     self.location_mapping[html_file] = f"part-{index}.html"

        for index, image_file in enumerate(self.image_files.keys()):
            directoryless_image_file = image_file.split("/")[-1]
            image_format = directoryless_image_file.split(".")[-1]

            new_image_name = f"image-{str(uuid.uuid4())}"
            new_image_location = f"{new_image_name}.{image_format}"
            self.location_mapping[directoryless_image_file] = new_image_location
            image_content = self.image_files[image_file]
            self.images.append(
                Image(location=new_image_location, content=image_content, format=image_format))

    def swap_locations_in_parsed_chapters(self):
        self.swap_images_in_parsed_chapters()
        self.swap_links_in_parsed_chapters()

    def swap_links_in_parsed_chapters(self):
        for chapter in self.raw_chapters:
            chapter: RawChapter
            items = chapter.content.find_all("a")
            for item in items:
                if "href" not in item.attrs:
                    item.attrs["href"] = "#"
                    continue

                src = item.attrs["href"].split("/")[-1]

                if src not in self.location_mapping:
                    item.attrs["href"] = "#"
                    continue

                new_src = self.location_mapping[src]
                item.attrs["href"] = new_src

    def swap_images_in_parsed_chapters(self):
        for chapter in self.raw_chapters:
            chapter: RawChapter
            items = chapter.content.find_all(["img", "image"])
            for item in items:

                src = item.attrs["src"].split("/")[-1]
                if src not in self.location_mapping:
                    continue

                new_src = self.location_mapping[src]
                item.attrs["src"] = f"/api/books/image/{new_src}"

    def convert_raws_to_output(self):
        for chapter in self.raw_chapters:
            chapter: RawChapter
            title = titlecase_chapter(chapter.title)
            new_chapter = Chapter(
                title=title,
                slug=title_to_slug(title),
                content=str(chapter.content.prettify()),
                order=chapter.order
            )
            self.chapters.append(new_chapter)

    def parse_chapters(self):
        for file_id in self.file_order:
            file = self.html_files[file_id]()

            if file_id in self.navpoints:
                navpoints = self.navpoints[file_id]
            else:
                self.carry_over("Other Content", copy.copy(
                    file.find("body")), file_id)
                continue

            for navpoint_id, navpoint in enumerate(navpoints):

                body, header, next_header = self.find_headers(
                    file, navpoint_id, navpoints)

                navpoint_references_entire_page = navpoint.selector == None

                if header:
                    if self.chapter_carry_over:
                        remainder_of_body = copy.copy(body)
                        # `header` references the header in `body`, `header_in_remainder` references the same header but in the `remainder_of_body` object instead
                        header_in_remainder = remainder_of_body.select_one(
                            f"#{header.attrs['id']}")
                        ContentParser.force_remove_including_after(
                            header_in_remainder)
                        self.carry_over(
                            navpoint.title, remainder_of_body, file_id)
                        self.push_carry_over()

                    ContentParser.remove_including_before(header)

                if next_header:
                    ContentParser.force_remove_including_after(next_header)
                else:
                    if not navpoint_references_entire_page:
                        # No next_header in this page. Merge into the carry over and look at the next page
                        self.carry_over(
                            navpoint.title, body, file_id)
                        continue

                self.carry_over(navpoint.title, body, file_id)
                self.push_carry_over()

        if self.chapter_carry_over:
            self.push_carry_over()

    def title_to_slug(self, title):
        return slugify(title)

    def add_ids_to_location_map(self, chapter: RawChapter, filename):
        content = chapter.content
        tags_with_an_id = content.find_all(id=True)
        filename = filename.split("/")[-1]
        for tag in tags_with_an_id:
            tag_id = tag.attrs["id"]
            ref = f"{filename}#{tag_id}"
            new_ref = f"{title_to_slug(chapter.title)}#{tag_id}"
            self.location_mapping[ref] = new_ref
        self.location_mapping[filename] = title_to_slug(chapter.title)

    def add_chapter(self, chapter: RawChapter):
        new_chapter = RawChapter(
            title=chapter.title,
            content=chapter.content,
            order=self.current_order
        )
        self.raw_chapters.append(new_chapter)
        self.current_order += 1

    def carry_over(self, title, to_merge, filename):
        if self.chapter_carry_over is None:
            self.chapter_carry_over = RawChapter(
                title=title, content=to_merge)
            self.add_ids_to_location_map(self.chapter_carry_over, filename)
            return

        for child in to_merge.find_all(recursive=False):
            self.chapter_carry_over.content.append(child)
        self.add_ids_to_location_map(self.chapter_carry_over, filename)

    def push_carry_over(self):
        if self.chapter_carry_over.title is None:
            self.chapter_carry_over.title = "Other Content"

        self.add_chapter(self.chapter_carry_over)
        self.chapter_carry_over = None

    def find_headers(self, file: BeautifulSoup, navpoint_id, navpoints):
        navpoint = navpoints[navpoint_id]

        next_navpoint = None
        if navpoint_id + 1 < len(navpoints):
            next_navpoint = navpoints[navpoint_id+1]

        body = copy.copy(file.find("body"))

        if navpoint.selector:
            header = body.select_one(f"#{navpoint.selector}")
        else:
            header = None

        if next_navpoint and next_navpoint.selector:
            next_header = body.select_one(f"#{next_navpoint.selector}")
        else:
            next_header = None

        return (body, header, next_header)

    @staticmethod
    def remove_including_before(target):
        # If the target is too complex (meaning it's likely to be the page we are trying to display), it won't be removed.
        curr_target = target
        while curr_target is not None:
            curr_target: bs4.Tag
            for prev_sibling in curr_target.find_previous_siblings():
                prev_sibling.decompose()
            curr_target = curr_target.parent
        ContentParser.remove_if_not_complex(target)

    @staticmethod
    def force_remove_including_after(target):
        # Will always remove the target.
        curr_target = target
        while curr_target is not None:
            target: bs4.Tag
            for prev_sibling in curr_target.find_next_siblings():
                prev_sibling.decompose()
            curr_target = curr_target.parent
        target.decompose()

    @staticmethod
    def remove_if_not_complex(target: bs4.Tag):
        children = target.find_all(recursive=True)
        if len(children) <= 1:
            target.decompose()
