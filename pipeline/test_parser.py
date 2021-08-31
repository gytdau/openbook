from typing import NamedTuple
import unittest
from bs4 import BeautifulSoup
from page_parser import PageParser
from unittest import TestCase
import os


def files_from_string(file_order: list, files_in_string: dict):
    files = {}
    for filename in file_order:
        files[filename] = BeautifulSoup(
            files_in_string[filename], features='lxml')

    return files


class Navpoint(NamedTuple):
    title: str
    selector: str


class TestPageParser(TestCase):
    def test_parses_one_page(self):
        file_order = ["tests/parser_test.html"]
        mocked_files = {
            "tests/parser_test.html":
            """<head>
    <title>Title</title>
</head>

<body>
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
</body>
    """}
        files = files_from_string(file_order, mocked_files)
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


if __name__ == "__main__":
    unittest.main()
