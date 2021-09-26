import json
import boto3
import base64
import os
from dotenv import dotenv_values

config = {
    **dotenv_values(".env"),  # load sensitive variables
    **os.environ,  # override loaded values with environment variables
}

bucket_name = config["BUCKET_NAME"] if 'BUCKET_NAME' in config else None
db_connection = config["DB_CONNECTION"] if 'DB_CONNECTION' in config else None

def test_event(event, context):
    return {
        'statusCode': 202,
        'body': json.dumps({'type' :type(event).__name__, 'event': event}),
    }
# this is triggered through an API,
# the API accepts a json (e.g {'id': [1,2,3,4]})
# once recieved this function will trigger a single async lambda `updateBook` per id
def UpdateBooks(event, context):
    # body = {"data": [{"book_id": 1, "ebook_source_id": 1}, ...]}

    data = event['data']
    responses = []
    client = boto3.client('lambda')
    for book in data:
        response = client.invoke(
            FunctionName='updateBook',
            InvocationType='Event',  # 'RequestResponse',
            Payload=json.dumps(book),
        )
        print(response['Payload'].read())
        del response['Payload']
        responses.append(response)

    print(event, context)
    return {
        'statusCode': 202,
        'body': json.dumps(responses),
    }


def UpdateBook(event, context):
    book_id = event['book_id']
    ebook_source_id = event['ebook_source_id']

    from db import db
    con = db(db_connection)

    ebook_source = con.get_book_source_by_id(ebook_source_id)
    if(not ebook_source):
        return {
            'statusCode': 200,
            'body': json.dump({'error': "ebook_source not found"})
        }

    import helpers
    url = helpers.parse_s3_url(ebook_source[3])
    epub = helpers.EpubParserFromS3(**url)

    book = con.get_book_by_ebook_source_id(ebook_source_id)
    if(not book):
        return {
            'statusCode': 200,
            'body': json.dump({'error': "book not found"})
        }

    if(ebook_source[0] != ebook_source_id or book[0] != book_id):
        return {
            'statusCode': 200,
            'body': json.dump({'error': "ids mismatch"})
        }

    con.add_chapters(book_id, epub.content.chapters)
    con.add_images(book_id, epub.content.images)

    return {
        'statusCode': 200,
        'body': event
    }


def DownloadBooks(event, context):
    # body = {"data": [{"gutenberg_id": 1}, ...]}

    data = event['data']
    responses = []
    client = boto3.client('lambda')
    for book in data:
        response = client.invoke(
            FunctionName='downloadBook',
            InvocationType='Event',  # 'RequestResponse',
            Payload=json.dumps(book),
        )
        print(response['Payload'].read())
        del response['Payload']
        responses.append(response)

    print(event, context)
    return {
        'statusCode': 202,
        'body': json.dumps(responses),
    }

# work around to s3 transfer closing buffer
# https://github.com/boto/s3transfer/issues/80#issuecomment-482534256
from io import BufferedReader
class NonCloseableBufferedReader(BufferedReader):
    def close(self):
        self.flush()

def DownloadBook(event, context):
    gutenberg_id = event['gutenberg_id']

    from db import db
    con = db(db_connection, False)

    import epub_downloader
    f, filename = epub_downloader.download_ebook_to_temp(gutenberg_id)

    import epub_parser
    epub = epub_parser.EpubParser(filename, f)
    if(not epub.can_be_unzipped()):
        raise ValueError(f"can't be unzipped, invalid epub file, {filename}")

    ebook_source = con.get_book_source_by_hash(epub.file_hash)
    if(not ebook_source):
        print("Uploading to S3")
        s3_client = boto3.resource('s3')
        f.seek(0)
        config = boto3.s3.transfer.TransferConfig(multipart_threshold=262144, max_concurrency=5, multipart_chunksize=262144, num_download_attempts=5, max_io_queue=5, io_chunksize=262144, use_threads=True)
        s3buffer = NonCloseableBufferedReader(f)
        response = s3_client.meta.client.upload_fileobj(
            s3buffer, bucket_name, filename, Config=config)
        s3buffer.detach()
        print("Uploaded")

        ebook_source_id = con.add_book_source(
            "gutenberg", filename, f"s3://{bucket_name}/{filename}", epub.file_hash)
    else:
        print("Skip Uploading")
        ebook_source_id = ebook_source[0]

    book_id = None
    if(ebook_source):
        book = con.get_book_by_ebook_source_id(ebook_source_id)
        if(book):
            book_id = book[0]

    epub.parse()
    if(not book_id):
        book_id = con.add_book(ebook_source_id, epub.title, epub.author,
                               epub.slug, epub.description, epub.publication)

    print("Proccessing Chapters")
    con.add_chapters(book_id, epub.content.chapters)
    print("Proccessing Images")
    con.add_images(book_id, epub.content.images)
    print("Done")

    event['book_id'] = book_id
    event['ebook_source_id'] = ebook_source_id
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }

def DownloadRangeBooks(event, context):
    # body = {"start": n, "end": m}

    start_id = event['start']
    end_id = event['end']

    responses = []
    client = boto3.client('lambda')

    import epub_downloader
    books = epub_downloader.get_csv_reader(False)

    for book in books:
        if(book['Type'] != 'Text'):
            continue

        book_id = int(book['Text#'])
        if(book_id >= start_id and book_id <= end_id):
            response = client.invoke(
                FunctionName='downloadBook',
                InvocationType='Event', #'RequestResponse',
                Payload=json.dumps({"gutenberg_id": book_id}),
            )
            print(f"Requesting book ({book_id}) download")

            del response['Payload']
            responses.append(response)

    return {
        'statusCode': 202,
        'body': json.dumps(responses),
    }

if __name__ == "__main__":
    res = DownloadBook("{\"gutenberg_id\": 1}", None)
    print(res)
    res = UpdateBook("{\"book_id\": 1, \"ebook_source_id\": 1}", None)
    print(res)
