from os import stat
from collections import deque
from bs4 import BeautifulSoup
import copy

import bs4


class PageParser(object):
    def __init__(self, pages, targets):
        self.pages = pages
        self.targets = targets

    def parse_into_pages(self):
        new_pages = {}
        for target in self.targets:
            new_pages[target] = None

        current_new_page = None
        current_target = 0
        # Assume targets are in order of the pages
        for page in self.pages:
            page: BeautifulSoup
            print("New page")
            if current_new_page:
                print("Carrying over")

            body, target, next_target = self.find_target(page, current_target)

            while target or current_new_page:
                if current_new_page:
                    if next_target:
                        PageParser.remove_all_next(next_target)
                        self.add_into_tag(current_new_page,
                                          body.find_all(recursive=False))
                        new_pages[self.targets[current_target]
                                  ] = current_new_page
                        current_new_page = None
                        current_target += 1
                        body, target, next_target = self.find_target(
                            page, current_target)
                        continue
                    else:
                        self.add_into_tag(current_new_page, body.children)
                        current_target += 1
                        break

                PageParser.remove_all_previous(target)

                if next_target:
                    PageParser.remove_all_next(next_target)
                else:
                    current_new_page = body
                    break

                new_pages[self.targets[current_target]] = body

                current_target += 1
                body, target, next_target = self.find_target(
                    page, current_target)

        if current_new_page:
            new_pages[self.targets[-1]] = current_new_page

        # TODO: Remove unnecessary re-parsing to make the output look neat. This is just for the tests to pass
        for target in self.targets:
            new_pages[target] = BeautifulSoup(
                str(new_pages[target]), 'lxml').select("body")

        return new_pages

    @staticmethod
    def add_into_tag(page, children):
        for child in children:
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

    @staticmethod
    def remove_all_previous(target):
        curr_target = target
        while curr_target is not None:
            curr_target: bs4.Tag
            for prev_sibling in curr_target.find_previous_siblings():
                prev_sibling.decompose()
            curr_target = curr_target.parent
        target.decompose()

    @staticmethod
    def remove_all_next(target):
        curr_target = target
        while curr_target is not None:
            target: bs4.Tag
            for prev_sibling in curr_target.find_next_siblings():
                prev_sibling.decompose()
            curr_target = curr_target.parent
        target.decompose()
