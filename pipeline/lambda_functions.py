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

# this is triggered through an API,
# the API accepts a json (e.g {'id': [1,2,3,4]})
# once recieved this function will trigger a single async lambda `updateBook` per id


def UpdateBooks(event, context):
    # body = {"data": [{"book_id": 1, "ebook_source_id": 1}, ...]}

    body = ""
    if(not event['isBase64Encoded']):
        body = json.loads(event['body'])
    else:
        body = json.loads(base64.b64decode(event['body']))

    responses = []
    client = boto3.client('lambda')
    for book in body['data']:
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
    data = json.loads(event)
    book_id = data['book_id']
    ebook_source_id = data['ebook_source_id']

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


def DownloadBook(event, context):
    # body = {"data": [{"gutenberg_id": 1}, ...]}

    body = ""
    if(not event['isBase64Encoded']):
        body = json.loads(event['body'])
    else:
        body = json.loads(base64.b64decode(event['body']))

    responses = []
    client = boto3.client('lambda')
    for book in body['data']:
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
    data = json.loads(event)
    gutenberg_id = data['gutenberg_id']

    from db import db
    con = db(db_connection)

    import epub_downloader
    filepath = epub_downloader.download_ebook(gutenberg_id)
    filename = os.path.basename(filepath)

    import epub_parser
    epub = epub_parser.EpubParser(filepath)
    ebook_source = con.get_book_source_by_hash(epub.file_hash)
    if(not ebook_source):
        s3_client = boto3.resource('s3')
        with open(filepath, 'rb') as f:
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


if __name__ == "__main__":
    res = DownloadBook("{\"gutenberg_id\": 1}", None)
    print(res)
    res = UpdateBook("{\"book_id\": 1, \"ebook_source_id\": 1}", None)
    print(res)
