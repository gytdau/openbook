from bs4 import BeautifulSoup
import copy

import bs4


class PageParser(object):
    def __init__(self, pages, targets):
        self.pages = pages
        self.targets = targets
        self.processed_pages = {}
        for target in self.targets:
            self.processed_pages[target] = None

    def parse_into_pages(self):
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

        # TODO: Remove unnecessary re-parsing to make the output look neat. This is just for the tests to pass
        for header in range(len(self.targets)):
            self.set_page(header, BeautifulSoup(
                str(self.processed_pages[self.targets[header]]), 'lxml').select("body"))

        return self.processed_pages

    def set_page(self, current_target, page):
        self.processed_pages[self.targets[current_target]] = page

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
