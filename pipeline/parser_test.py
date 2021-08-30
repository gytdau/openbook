from bs4 import BeautifulSoup
from page_parser import PageParser
from unittest import TestCase
import os


def expectation_into_bs4(dictionary: dict):
    for key in dictionary.keys():
        dictionary[key] = BeautifulSoup(
            dictionary[key], features='lxml')
        dictionary[key] = dictionary[key].select("body")
    return dictionary


def load_files(files: list):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    pages = []
    for filename in files:
        with open(os.path.join(dir_path, filename)) as f:
            pages.append(BeautifulSoup(f, features='lxml'))
    return pages


def test_parses_one_page():
    pages = load_files(["tests/parser_test.html"])
    parser = PageParser(pages, ["t1", "t2", "t3"])
    result = parser.parse_into_pages()
    expectation = {
        't1':
            """<body>
            <div>
            <h1 id="t1">Title 1</h1>
            </div>
            <div>
            <span>1.1</span>
            <div>
            <span>1.2</span>
            </div>
            </div>
            </body>""",
        't2':
            """<body>
            <div>
            <h1 id="t2">Title 2</h1>
            </div>
            <div>
            <span>2.1</span>
            </div>
            </body>""",
        't3':
            """<body>
            <div>
            <h2 id="t3">Title 3</h2>
            <p>3.1</p>
            </div>
            <span>
            <p>3.2</p>
            </span>
            </body>"""
    }
    expectation = expectation_into_bs4(expectation)
    TestCase().assertDictEqual(result, expectation)


def test_parses_two_pages():
    pages = load_files(
        ["tests/parser_test.html", "tests/parser_test_part_2.html"])
    parser = PageParser(pages, ["t1", "t2", "t3", "t4"])
    result = parser.parse_into_pages()
    expectation = {
        't1':
            """<body>
            <div>
            <h1 id="t1">Title 1</h1>
            </div>
            <div>
            <span>1.1</span>
            <div>
            <span>1.2</span>
            </div>
            </div>
            </body>""",
        't2':
            """<body>
            <div>
            <h1 id="t2">Title 2</h1>
            </div>
            <div>
            <span>2.1</span>
            </div>
            </body>""",
        't3':
            """<body>
            <div>
            <h2 id="t3">Title 3</h2>
            <p>3.1</p>
            </div>
            <span>
            <p>3.2</p>
            </span>
            <div>
            <span>3.3</span>
            </div></body>""",
        't4':
            """<body>
            <div>
            <h1 id="t4">Title 4</h1>
            </div>
            <div>
            <span>4.1</span>
            </div>
            </body>"""
    }
    expectation = expectation_into_bs4(expectation)
    TestCase().assertDictEqual(result, expectation)


if __name__ == "__main__":
    test_parses_one_page()
    test_parses_two_pages()
