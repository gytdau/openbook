rsync -avm --del --dry-run --stats --include='*-images.epub' -f 'hide,! */' aleph.gutenberg.org::gutenberg-epub "/media/gytdau/Filestore/gutenberg

# process

Process an epub to the output format. The output folder contains a manifest in sqlite3 format

For help try `python3 process.py -h`

# benchmark

Loop the `process` function and see how fast it performs, giving you an idea of how fast the entire book catalog could be converted.

(I get 0.2s/book, which is about ~4 hours for the catalog)