from bs4 import BeautifulSoup
from typing import List, Dict, NamedTuple, Tuple
import copy

import bs4


class PageParser(object):
    def __init__(self, file_order: List[str], files: Dict[str, BeautifulSoup], navpoints: Dict[str, List[NamedTuple('Navpoint', title=str, selector=str)]]):
        # file_order: [file_id, ...]
        # File order is derived from the spine of content.opf

        # files: { file_id: BeautifulSoup_page }
        # Contains the HTML files as BS4 classes

        # navpoints: { file_id: [{title, selector}, {title, selector}, ...] }
        # Navpoints are sorted into their files in this dictionary. Each navpoint is represented as a named tuple
        # navpoint.selector can be None to mean it begins at the top of the page

        # TODO: Process links in files
        # TODO: Process images in files
        self.file_order = file_order
        self.files = files
        self.navpoints = navpoints
        self.processed_pages = []
        self.carry_over_page = None

    def parse_into_pages(self):
        for file_id in self.file_order:
            file = self.files[file_id]

            if file_id in self.navpoints:
                navpoints = self.navpoints[file_id]
            else:
                self.merge_into_carry_over(None, copy.copy(file.find("body")))
                continue

            for navpoint_id, navpoint in enumerate(navpoints):

                body, header, next_header = self.find_headers(
                    file, navpoint_id, navpoints)

                navpoint_references_entire_page = navpoint.selector == None

                if header:
                    if self.carry_over_page:
                        remainder_of_body = copy.copy(body)
                        # `header` references the header in `body`, `header_in_remainder` references the same header but in the `remainder_of_body` object instead
                        header_in_remainder = remainder_of_body.select_one(
                            f"#{header.attrs['id']}")
                        PageParser.remove_including_after(header_in_remainder)
                        self.merge_into_carry_over(None, remainder_of_body)
                        self.commit_carry_over()

                    PageParser.remove_including_before(header)

                if next_header:
                    PageParser.remove_including_after(next_header)
                else:
                    if not navpoint_references_entire_page:
                        # No next_header in this page. Merge into the carry over and look at the next page
                        self.merge_into_carry_over(navpoint.title, body)
                        continue

                self.add_page(navpoint.title, body)

        if self.carry_over_page:
            self.commit_carry_over()

        return self.processed_pages

    def add_page(self, title, page):
        self.processed_pages.append((title, page.prettify()))

    def merge_into_carry_over(self, title, to_merge):
        if self.carry_over_page == None:
            self.carry_over_page = (title, to_merge)
            return

        for child in to_merge.find_all(recursive=False):
            self.carry_over_page[1].append(child)

    def commit_carry_over(self):
        if self.carry_over_page[0]:
            title = self.carry_over_page[0]
        else:
            title = "Other Content"

        self.add_page(title, self.carry_over_page[1])
        self.carry_over_page = None

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

    @ staticmethod
    def remove_including_before(target):
        curr_target = target
        while curr_target is not None:
            curr_target: bs4.Tag
            for prev_sibling in curr_target.find_previous_siblings():
                prev_sibling.decompose()
            curr_target = curr_target.parent
        target.decompose()

    @ staticmethod
    def remove_including_after(target):
        curr_target = target
        while curr_target is not None:
            target: bs4.Tag
            for prev_sibling in curr_target.find_next_siblings():
                prev_sibling.decompose()
            curr_target = curr_target.parent
        target.decompose()
