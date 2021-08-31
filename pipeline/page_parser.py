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
        self.processed_pages = {}
        for target in self.targets:
            self.processed_pages[target] = None

    def parse_into_pages(self):
        carry_over_page = None

        for file_id in self.file_order:
            file = self.files[file_id]
            navpoints = self.navpoints[file_id]

            if len(navpoints) == 0:
                carry_over_page = file

        carry_over_page = None
        current_header_num = 0
        # Assume targets are in order of the pages
        for page in self.pages:
            page: BeautifulSoup
            print("New page")
            if carry_over_page:
                print("Carrying over")

            body, header, next_header = self.find_headers(
                page, current_header_num)

            while header or carry_over_page:
                if carry_over_page:
                    if next_header:
                        PageParser.remove_including_after(next_header)
                        self.merge(carry_over_page,
                                   body)
                        self.set_page(current_header_num, carry_over_page)
                        carry_over_page = None
                        current_header_num += 1
                        body, header, next_header = self.find_headers(
                            page, current_header_num)
                        continue
                    else:
                        self.merge(carry_over_page, body)
                        break

                PageParser.remove_including_before(header)

                if next_header:
                    PageParser.remove_including_after(next_header)
                else:
                    carry_over_page = body
                    break

                self.set_page(current_header_num, body)

                current_header_num += 1
                body, header, next_header = self.find_headers(
                    page, current_header_num)

        if carry_over_page:
            self.set_page(-1, carry_over_page)

        return self.processed_pages

    def set_page(self, current_target, page: BeautifulSoup):
        self.processed_pages[self.targets[current_target]] = page.prettify()

    @ staticmethod
    def merge(target_tag, from_tag):
        for child in from_tag.find_all(recursive=False):
            target_tag.append(child)

    def find_headers(self, page: BeautifulSoup, current_target):
        if len(self.targets) == current_target:
            return (None, None, None)

        body = copy.copy(page.find("body"))
        target = body.select_one(f"#{self.targets[current_target]}")

        if len(self.targets) == current_target + 1:
            next_target = None
        else:
            next_target = body.select_one(
                f"#{self.targets[current_target + 1]}")

        return (body, target, next_target)

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
