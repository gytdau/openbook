import os
from epub_parser import EpubParser

location = "epubs/pg66057-images.epub"
script_location = os.path.dirname(os.path.realpath(__file__))
location = os.path.join(script_location, location)

parsed = EpubParser().from_file(location)

print(parsed)
