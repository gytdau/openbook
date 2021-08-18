import sys
import json
import os
from bs4 import BeautifulSoup
import shutil
from slugify import slugify
import random

filename = sys.argv[1]

manifest = {}
os.makedirs("output", exist_ok=True)


def normalize_navlink_src(filename):
    if "#" in filename:
        # A selector is at the end. Remove it. TODO: Figure out why?
        filename = filename.split("#")[0]
    return filename


def process_chapter(chapter: BeautifulSoup, filename, slug):
    body = chapter.find("body")
    body.name = "div"
    body = str(body)
    result_path = f'output/{slug}/{filename}'
    with open(result_path, "w") as f:
        f.write(body)
    return result_path


def process_epub(filename):
    filename_without_extension = filename.split(".")[0]

    shutil.unpack_archive(filename, filename_without_extension, "zip")

    # todo: extract author and title

    def get_file(filename, relative_to=None):

        if relative_to:
            relative_to = os.path.dirname(relative_to)
            filename = os.path.join(relative_to, filename)

        with open(f'{filename_without_extension}/{filename}') as f:
            return (BeautifulSoup(f, features="lxml"), filename)

    container, _ = get_file("META-INF/container.xml")
    content, content_path = get_file(
        container.find("rootfile").attrs["full-path"])

    title = content.find("dc:title").text
    description_element = content.find("dc:description")
    description = description_element.text if description_element else ""
    author = content.find("dc:creator").text

    slug = f'{slugify(title)}_{random.randint(0, 1000)}'
    os.makedirs(f'output/{slug}', exist_ok=True)

    ncx, ncx_path = get_file(content.select_one(
        "#ncx").attrs["href"], content_path)
    # print(ncx)
    chapters = []

    for navpoint in ncx.find_all("navpoint"):
        # Todo: sort by playorder attribute of navpoints.
        navpoint: BeautifulSoup
        # print(navpoint)
        chapter_title = navpoint.find("text").text
        chapter_path = normalize_navlink_src(
            navpoint.find("content").attrs["src"])
        chapter, _ = get_file(
            chapter_path, content_path)

        result_path = process_chapter(chapter, chapter_path, slug)

        chapters.append({
            'title': chapter_title,
            'src': result_path,
        })

    shutil.rmtree(filename_without_extension)
    manifest[slug] = {
        'title': title,
        'description': description,
        'author': author,
        'slug': slug,
        'chapters': chapters,
    }


process_epub(filename)

with open('output/manifest.json', 'w') as f:
    f.write(json.dumps(manifest))
