import sys
from epub_parser import EpubParser
from db import db
import os
import shutil
import argparse
from pathlib import Path
from dotenv import dotenv_values

config = {
    **dotenv_values(".env"),  # load sensitive variables
    **os.environ,  # override loaded values with environment variables
}

parser = argparse.ArgumentParser(description='Process ebook or ebooks')

parser.add_argument('--keep', action='store_true',
                    help="Do not delete the database and output before starting")
parser.add_argument('--input-dir', default=None,
                    help="Gutenberg archive directory to convert")
parser.add_argument('--input-path', default=None,
                    help="Individual epub to convert")
parser.add_argument('--max', type=int, default=None,
                    help="Maximum books to convert in this run")
parser.add_argument('--dry-run', action='store_true',
                    help="Do not make any changes, simply list stats about what you will change")

args = parser.parse_args()
db_connection = config['DB_CONNECTION']

if not args.keep:
    db(db_connection, False).drop_tables()

if args.input_path:
    files = [args.input_path]
elif args.input_dir:
    files = tuple(Path(args.input_dir).rglob("*.epub"))
    if args.max:
        files = files[:args.max]
else:
    parser.error(
        "no input specified, you must specify one of the following arguments --input-dir or --input-path")

print(f"Found {len(files)} files")

if args.dry_run:
    for file in files:
        print(file)

if not args.dry_run:
    con = db(db_connection)
    for file in files:
        epub = EpubParser(file).parse()

        if not epub:
            print(f"warning: ({file}) not a valid epub")
            continue

        book_id = con.add_book(epub.title, epub.author,
                               epub.slug, epub.description)

        con.add_chapters(book_id, epub.chapters)
