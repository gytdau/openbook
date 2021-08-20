import sys
from helpers import process_epubs
import sqlite3
import os
import shutil
import argparse
from pathlib import Path

default_output_directory = "../interface/service/public/output"
default_database_directory = '../interface/service/database.sqlite3'

parser = argparse.ArgumentParser(description='Process ebook or ebooks')

parser.add_argument('--output', default=default_output_directory,
                    help="Folder where the resulting files go")
parser.add_argument('--database', default=default_database_directory,
                    help="Location to save sqlite3 database")
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

output_directory = args.output
database_directory = args.database

# TODO: make this script support continuing a previously stopped job
if not args.keep:
    if os.path.exists(output_directory):
        if args.dry_run:
            print(f"Would delete {output_directory}")
        else:
            shutil.rmtree(output_directory)

    if os.path.exists(database_directory):
        if args.dry_run:
            print(f"Would delete {database_directory}")
        else:
            os.remove(database_directory)

os.makedirs(output_directory, exist_ok=True)
con = sqlite3.connect(database_directory)

if args.input_path:
    files = [args.input_path]
elif args.input_dir:
    files = tuple(Path(args.input_dir).rglob("*.epub"))
    if args.max:
        files = files[:args.max]
else:
    print("No input specified")
    sys.exit()

print(f"Found {len(files)} files")
for file in files:
    print(file)

if not args.dry_run:
    process_epubs(files, con, output_directory)
