import sys
from helpers import process_epubs
import sqlite3
import os

os.makedirs("output", exist_ok=True)
con = sqlite3.connect('output/manifest.sqlite3')

filename = sys.argv[1]
process_epubs([filename], con)
