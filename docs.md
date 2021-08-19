# epub format

## epub versions

epub 2 was published some time ago
epub 3 is billed as a "cleaner variant"

calibre can convert epub 2 to epub 3
we could convert every epub2 book we find. what's the additional processing time of this? this could be doable

there is a book called "EPUB 3 Best Practices" on O'Reilly Online Library!!
good to look at?

## toc.ncx

mandatory in epub-2
superseeded in epub-3 by toc.xhtml, which is a xhtml standard (but I think most/all(?) epubs include .ncx for compatability)

It provides the table of contents

There is no nesting allowed in toc.ncx (because readers don't support it, though technically it is allowed)
but there is nesting in toc.xhtml

## chapters

Appears to be one chapter per page; perhaps this is an assumption that needs to be tested?

## content.opf

