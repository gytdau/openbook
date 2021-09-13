import json
import boto3
import base64
import os
from dotenv import dotenv_values

config = {
    **dotenv_values(".env"),  # load sensitive variables
    **os.environ,  # override loaded values with environment variables
}

bucket_name = config["BUCKET_NAME"]
db_connection = config["DB_CONNECTION"]

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


def DownloadBook(event, context):
    gutenberg_id = event['gutenberg_id']

    from db import db
    con = db(db_connection)

    import epub_downloader
    f, filename = epub_downloader.download_ebook_to_memory(gutenberg_id)

    import epub_parser
    epub = epub_parser.EpubParser(filename, f)
    ebook_source = con.get_book_source_by_hash(epub.file_hash)
    if(not ebook_source):
        s3_client = boto3.resource('s3')
        f.seek(0)
        response = s3_client.meta.client.upload_fileobj(
            f, bucket_name, filename)
        ebook_source_id = con.add_book_source(
            "gutenberg", filename, f"s3://{bucket_name}/{filename}", epub.file_hash)
    else:
        ebook_source_id = ebook_source[0]

    book_id = None
    if(ebook_source):
        book = con.get_book_by_ebook_source_id(ebook_source_id)
        book_id = book[0]

    if(not book_id):
        book_id = con.add_book(ebook_source_id, epub.title, epub.author,
                               epub.slug, epub.description)

    con.add_chapters(book_id, epub.content.chapters)
    con.add_images(book_id, epub.content.images)

    data['book_id'] = book_id
    data['ebook_source_id'] = ebook_source_id
    return {
        'statusCode': 200,
        'body': json.dumps(data)
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
