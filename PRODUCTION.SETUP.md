# Production Setup

## Production Enviroment
While this project can be setup using different enviroment, we chose to use AWS & Heroku,
As such this setup guide will only address those 2 enviroments.

Note: AWS IAM allows for finely controlled user access

## Requirements
- Basic Knowledge of Heroku & AWS CLI, IAM, S3, RDS & Lambda
- [PostgreSQL](https://www.postgresql.org/download/) (recommended v13.x)
- [NodeJS/npm](https://nodejs.org/en/download/)
- [Python3](https://www.python.org/downloads/) (Recommended v3.7.x)

### Setup
- AWS DB
    - Setup PostgreSQL DB on AWS with user/pass for production access
- AWS Lambda
  - Preparing Lambda Layer
    - Requires linux enviroment & matching lambda python version
    - `cd pipeline`
    - `cp requirements.txt lambda_requirements.txt`
    - `sed -i 's/psycopg2/psycopg2-binary/g' lambda_requirements.txt`
    - `sed -i '/^boto/d' lambda_requirements.txt`
    - `pip3 install virtualenv`
    - `python3 -m venv ./venv`
    - `source venv/bin/activate`
    - `pip3 install -r lambda_requirements.txt`
    - `deactivate`
    - `mv ./venv/python$PYTHON_VERSION/site-packages/ python/`
    - `zip -r lambda_layer.zip python/`
    - `aws lambda publish-layer-version --layer-name lambda_python_dep_layer --description "lambda python dep layer"  --zip-file fileb://lambda_layer.zip --compatible-runtimes python3.7 --compatible-architectures x86_64`
      - please note `LayerVersionArn` in the `stdout`
    - Attaching Layer to Lambda Function
      - Note before this step can be execute, the Lambda function must exist 
      - `aws lambda update-function-configuration --function-name downloadBook --layers $LayerVersionArn`
      - `aws lambda update-function-configuration --function-name downloadBooks --layers $LayerVersionArn`
      - `aws lambda update-function-configuration --function-name downloadRangeBooks --layers $LayerVersionArn`
      - `aws lambda update-function-configuration --function-name updateBook --layers $LayerVersionArn`
      - `aws lambda update-function-configuration --function-name updateBooks --layers $LayerVersionArn`
    - Cleanup
      - `rm -rf lambda_layer.zip python/ venv/` 
      - `cd ..`
  - Preparing/Creating/Updating Lambda Functions
    - Prepare 
      - `cd pipeline/`
      - `zip -r ../function.zip .`
    - Creating (Required during initial setup only)
      - IAM: we'd need an IAM role that allows the lambda function to execute and also access S3 bucket (We'll refer to it as lambda_s3)
      - `aws lambda create-function --function-name downloadBook --zip-file fileb://function.zip --handler lambda_functions.downloadBook --runtime python3.7 --role lambda_s3`
      - `aws lambda create-function --function-name downloadBooks --zip-file fileb://function.zip --handler lambda_functions.downloadBooks --runtime python3.7 --role lambda_s3`
      - `aws lambda create-function --function-name downloadRangeBooks --zip-file fileb://function.zip --handler lambda_functions.downloadRangeBooks --runtime python3.7 --role lambda_s3`
      - `aws lambda create-function --function-name updateBook --zip-file fileb://function.zip --handler lambda_functions.updateBook --runtime python3.7 --role lambda_s3`
      - `aws lambda create-function --function-name updateBooks --zip-file fileb://function.zip --handler lambda_functions.updateBooks --runtime python3.7 --role lambda_s3`
    - Updating Lambda function (Required during subsequent function update)
      - `aws lambda update-function-code --function-name updateBooks --zip-file fileb://aws-lambda.zip`
      - `aws lambda update-function-code --function-name updateBook --zip-file fileb://aws-lambda.zip`
      - `aws lambda update-function-code --function-name downloadRangeBooks --zip-file fileb://aws-lambda.zip`
      - `aws lambda update-function-code --function-name downloadBooks --zip-file fileb://aws-lambda.zip`
      - `aws lambda update-function-code --function-name downloadBook --zip-file fileb://aws-lambda.zip`

- Heroku
 - Setup a github hook to Heroku to allow automatic deployment

### Populating DB
The epub parsing and db population is all done through AWS Lambda, and since we've already set that app, all we need to do is invoke those functions
- Add/Update new single book to collection: `aws lambda invoke --function-name DownloadBook --payload '{ "gutenberg_id": 1 }'`
- Add/Update new multiple books to collection: `aws lambda invoke --function-name DownloadBooks --payload '{"data": [{"gutenberg_id": 1}, {"gutenberg_id": 2}]}'`
- Add/Update new range of books to collection: `aws lambda invoke --function-name DownloadRangeBooks --payload '{"start": 1, "end": 40000}'`
- To Update a book, while avoiding redownload
  - Single Book: `aws lambda invoke --function-name UpdateBook --payload '{ "book_id": 1, "ebook_source_id": 1 }'`
  - Multiple Book: `aws lambda invoke --function-name UpdateBooks --payload '{"data": [{"book_id": 1, "ebook_source_id": 1}, {"book_id": 2, "ebook_source_id": 2}]}'`
