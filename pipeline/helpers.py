
def join_path(path, filename):
    """
    epub path are unix based, we require this method for this to work correctly on windows
    """
    return '/'.join([path, filename])

def parse_s3_url(s3url):
    from urllib.parse import urlparse
    url = urlparse(s3url)

    if(url.scheme.casefold() != 's3'):
        print(f"Warning: not a valid s3 url ({s3url})")

    bucketname = url.netloc
    filename = url.path.lstrip('/')
    return {'bucketname': bucketname, 'filename': filename}

def EpubParserFromS3(bucketname, filename):
    # we are importing from within a function,
    # to avoid introducing unneeded dependencies when other simpler functions are called,
    # e.g join_path
    import boto3
    import io
    from epub_parser import EpubParser

    s3_client = boto3.resource('s3')
    book_object = s3_client.Object(bucketname, filename)
    book_io =  io.BytesIO()
    book_object.download_fileobj(book_io)
    return EpubParser(filename, book_io)