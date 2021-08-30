from os import stat
from collections import deque
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
        current_target = 0
        # Assume targets are in order of the pages
        for page in self.pages:
            page: BeautifulSoup
            print("New page")
            if carry_over_page:
                print("Carrying over")

            body, target, next_target = self.find_target(page, current_target)

            while target or carry_over_page:
                if carry_over_page:
                    if next_target:
                        PageParser.remove_all_next(next_target)
                        self.merge(carry_over_page,
                                   body)
                        self.set_page(current_target, carry_over_page)
                        carry_over_page = None
                        current_target += 1
                        body, target, next_target = self.find_target(
                            page, current_target)
                        continue
                    else:
                        self.merge(carry_over_page, body)
                        current_target += 1
                        break

                PageParser.remove_all_previous(target)

                if next_target:
                    PageParser.remove_all_next(next_target)
                else:
                    carry_over_page = body
                    break

                self.set_page(current_target, body)

                current_target += 1
                body, target, next_target = self.find_target(
                    page, current_target)

        if carry_over_page:
            self.set_page(-1, carry_over_page)

        # TODO: Remove unnecessary re-parsing to make the output look neat. This is just for the tests to pass
        for target in range(len(self.targets)):
            self.set_page(target, BeautifulSoup(
                str(self.processed_pages[self.targets[target]]), 'lxml').select("body"))

        return self.processed_pages

    def set_page(self, current_target, page):
        self.processed_pages[self.targets[current_target]] = page

    @ staticmethod
    def merge(page, body):
        for child in body.find_all(recursive=False):
            page.append(child)

    def find_target(self, page: BeautifulSoup, current_target):
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
    def remove_all_previous(target):
        curr_target = target
        while curr_target is not None:
            curr_target: bs4.Tag
            for prev_sibling in curr_target.find_previous_siblings():
                prev_sibling.decompose()
            curr_target = curr_target.parent
        target.decompose()

    @ staticmethod
    def remove_all_next(target):
        curr_target = target
        while curr_target is not None:
            target: bs4.Tag
            for prev_sibling in curr_target.find_next_siblings():
                prev_sibling.decompose()
            curr_target = curr_target.parent
        target.decompose()
