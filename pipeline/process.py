import sys
from helpers import process_epubs
import sqlite3
import os
import shutil

# TODO: make these into args
output_directory = "../interface/service/public/output"
database_directory = '../interface/service/database.sqlite3'

# TODO: make deleting into option
# TODO: make this script support continuing a previously stopped job
if os.path.exists(output_directory):
    shutil.rmtree(output_directory)

if os.path.exists(database_directory):
    os.remove(database_directory)

os.makedirs(output_directory, exist_ok=True)
con = sqlite3.connect(database_directory)


filename = sys.argv[1]
process_epubs([filename], con, output_directory)
