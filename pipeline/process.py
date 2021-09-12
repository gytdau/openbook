import sys
from epub_parser import EpubParser
from itertools import chain
from glob import glob
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

parser.add_argument('--drop', action='store_true',
                    help="Delete the database and output before starting")
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
BUCKET_NAME = "gutenberg-vivlia"

if args.drop:
    db(db_connection, False).drop_tables()

if args.input_path:
    files = [args.input_path]
elif args.input_dir:
    files = (chain.from_iterable(
        glob(os.path.join(x[0], '*.epub')) for x in os.walk(args.input_dir)))
else:
    parser.error(
        "no input specified, you must specify one of the following arguments --input-dir or --input-path")


if args.dry_run:
    for file in files:
        print(file)

if not args.dry_run:
    con = db(db_connection)
    processed = 0
    for file in files:
        processed += 1
        if args.max and processed >= args.max:
            break

        try:
            epub = EpubParser(file)
        except KeyboardInterrupt:
            sys.exit()
            pass
        except Exception as e:
            # You can delete these lines if debugging is annoying.
            print(e)
            continue

        if not epub:
            print(f"warning: ({file}) not a valid epub")
            continue

        source = con.get_book_source(epub.file_hash)
        if(not source):
            book_id = con.add_book(epub.title, epub.author,
                                epub.slug, epub.description)

            filename = os.path.basename(file)
            source = con.add_book_source(book_id, "gutenberg", filename, f"s3://{BUCKET_NAME}/{filename}", epub.file_hash)

        else:
            book_id = source[1]

        con.add_chapters(book_id, epub.content.chapters)
        con.add_images(book_id, epub.content.images)
