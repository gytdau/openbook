from typing import NamedTuple
import unittest
from bs4 import BeautifulSoup
from page_parser import PageParser
from unittest import TestCase
import os


def print_result(result):
    for pair in result:
        print(pair)


def scaffold(text):
    return BeautifulSoup(f"""<head>
    <title>Title</title>
</head>
<body>
{text}
</body>""")


class Navpoint(NamedTuple):
    title: str
    selector: str


class TestPageParser(TestCase):
    def test_parses_one_page(self):
        file_order = ["tests/parser_test.html"]
        files = {
            "tests/parser_test.html":
            scaffold("""
    <div>
        <span>Copyright Notice</span>
        <h1 id="t1">Title 1</h1>
    </div>
    <div>
        <span>1.1</span>
        <div>
            <span>1.2</span>
        </div>
        <h1 id="t2">Title 2</h1>
    </div>
    <div>
        <span>2.1</span>
        <h2 id="t3">Title 3</h2>
        <p>3.1</p>
    </div>
    <span>
        <p>3.2</p>
    </span>
    """)}
        navpoints = {
            "tests/parser_test.html": [
                Navpoint(title="My First Title", selector="t1"),
                Navpoint(title="My Second Title", selector="t2"),
                Navpoint(title="My Third Title", selector="t3"),
            ]
        }
        parser = PageParser(file_order, files, navpoints)

        result = parser.parse_into_pages()
        expectation = [
            ('My First Title', '<body>\n <div>\n </div>\n <div>\n  <span>\n   1.1\n  </span>\n  <div>\n   <span>\n    1.2\n   </span>\n  </div>\n </div>\n</body>'),
            ('My Second Title', '<body>\n <div>\n </div>\n <div>\n  <span>\n   2.1\n  </span>\n </div>\n</body>'),
            ('My Third Title', '<body>\n <div>\n  <p>\n   3.1\n  </p>\n </div>\n <span>\n  <p>\n   3.2\n  </p>\n </span>\n</body>')
        ]
        self.assertListEqual(result, expectation)

    def test_combines_unreferenced_page(self):
        file_order = ["one.html", "two.html", "three.html"]
        files = {
            "one.html":
            scaffold("""
    <div>
        <span>Copyright Notice</span>
        <h1 id="t1">Title 1</h1>
    </div>
    <div>
        <span>1.1</span>
    </div>
    """),
            "two.html":
            scaffold("""
    <div>
        <span>2.1</span>
    </div>
    """),
            "three.html":
            scaffold("""
    <div>
        <span>2.2</span>
        <h2 id="t2">Title 2</h2>
        <span>3.1</span>
    </div>
    """)}
        navpoints = {
            "one.html": [
                Navpoint(title="My First Title", selector="t1"),
            ],
            "three.html": [
                Navpoint(title="My Second Title", selector="t2"),
            ]
        }
        parser = PageParser(file_order, files, navpoints)

        result = parser.parse_into_pages()
        expectation = [
            ('My First Title', '<body>\n <div>\n </div>\n <div>\n  <span>\n   1.1\n  </span>\n </div>\n <div>\n  <span>\n   2.1\n  </span>\n </div>\n <div>\n  <span>\n   2.2\n  </span>\n </div>\n</body>'),
            ('My Second Title',
             '<body>\n <div>\n  <span>\n   3.1\n  </span>\n </div>\n</body>')
        ]
        self.assertListEqual(result, expectation)

    def test_combines_unreferenced_page_even_when_it_is_the_last_page(self):
        file_order = ["one.html", "two.html"]
        files = {
            "one.html":
            scaffold("""
    <div>
        <span>Copyright Notice</span>
        <h1 id="t1">Title 1</h1>
    </div>
    <div>
        <span>1.1</span>
    </div>
    """),
            "two.html":
            scaffold("""
    <div>
        <span>2.1</span>
    </div>
    """)}
        navpoints = {
            "one.html": [
                Navpoint(title="My First Title", selector="t1"),
            ],
        }
        parser = PageParser(file_order, files, navpoints)

        result = parser.parse_into_pages()
        expectation = [
            ('My First Title', '<body>\n <div>\n </div>\n <div>\n  <span>\n   1.1\n  </span>\n </div>\n <div>\n  <span>\n   2.1\n  </span>\n </div>\n</body>'),
        ]
        self.assertListEqual(result, expectation)

    def test_without_any_selectors(self):
        file_order = ["one.html", "two.html"]
        files = {
            "one.html":
            scaffold("""
    <div>
        <span>Copyright Notice</span>
        <h1>Title 1</h1>
    </div>
    <div>
        <span>1.1</span>
    </div>
    """),
            "two.html":
            scaffold("""
    <div>
        <h1>Title 2</h1>
        <span>2.1</span>
    </div>
    """)}
        navpoints = {
            "one.html": [
                Navpoint(title="My First Title", selector=None),
            ],
            "two.html": [
                Navpoint(title="My Second Title", selector=None),
            ],
        }
        parser = PageParser(file_order, files, navpoints)

        result = parser.parse_into_pages()
        expectation = [
            ('My First Title', '<body>\n <div>\n  <span>\n   Copyright Notice\n  </span>\n  <h1>\n   Title 1\n  </h1>\n </div>\n <div>\n  <span>\n   1.1\n  </span>\n </div>\n</body>'),
            ('My Second Title', '<body>\n <div>\n  <h1>\n   Title 2\n  </h1>\n  <span>\n   2.1\n  </span>\n </div>\n</body>')
        ]
        self.assertListEqual(result, expectation)


if __name__ == "__main__":
    unittest.main()
