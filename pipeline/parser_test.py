from bs4 import BeautifulSoup
from page_parser import PageParser
from unittest import TestCase
import os


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
 </div>
 <div>
  <span>
   1.1
  </span>
  <div>
   <span>
    1.2
   </span>
  </div>
 </div>
</body>""",
        't2':
            """<body>
 <div>
 </div>
 <div>
  <span>
   2.1
  </span>
 </div>
</body>""",
        't3':
            """<body>
 <div>
  <p>
   3.1
  </p>
 </div>
 <span>
  <p>
   3.2
  </p>
 </span>
</body>"""
    }
    TestCase().assertDictEqual(result, expectation)


def test_parses_two_pages():
    pages = load_files(
        ["tests/parser_test.html", "tests/parser_test_part_2.html"])
    parser = PageParser(pages, ["t1", "t2", "t3", "t4"])
    result = parser.parse_into_pages()
    expectation = {
        't1': """<body>
 <div>
 </div>
 <div>
  <span>
   1.1
  </span>
  <div>
   <span>
    1.2
   </span>
  </div>
 </div>
</body>""",
        't2': """<body>
 <div>
 </div>
 <div>
  <span>
   2.1
  </span>
 </div>
</body>""",
        't3': """<body>
 <div>
  <p>
   3.1
  </p>
 </div>
 <span>
  <p>
   3.2
  </p>
 </span>
 <div>
  <span>
   3.3
  </span>
 </div>
</body>""",
        't4': """<body>
 <div>
 </div>
 <div>
  <span>
   4.1
  </span>
 </div>
</body>"""
    }
    TestCase().assertDictEqual(result, expectation)


if __name__ == "__main__":
    test_parses_one_page()
    test_parses_two_pages()
