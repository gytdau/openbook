# Local/Dev Setup

## Requirements
- [PostgreSQL](https://www.postgresql.org/download/) (recommended v13.x)
- [NodeJS/npm](https://nodejs.org/en/download/)
- [Python3](https://www.python.org/downloads/) (Recommended v3.7.x)

### Initial Backend Setup
- install Python3 & PostgreSQL Requirements as listed above
- setup a postgreSQL database with user/pass for project access
- `cp pipeline/.env.example pipeline/.env`
- edit `.env` with appropriate access keys, users and passwords
- Python3 setup
  - Setup Dependencies 
    - `cd pipeline/`
    - `pip3 install -r requirements.txt`
    - `cd ..`
  - Create DB
    - `cd pipeline/`
    - `python3 db.py`

### Initial Frontdnd Setup
- install NodeJS/npm Requirements as listed above
- `cp pipeline/.env.example interface/service/.env`
- edit `.env` with appropriate access keys, users and passwords
- NodeJS setup
  - Setup Dependencies 
    - `npm install`

### Starting Server & Frontend
-  The server and frontend cmds should run in seperate terminal windows
-  Backend (API) Server: `npm start`
-  Frontend: `npm run start-interface`

### Popluating The DB with new epub entries
- To add a book into the db, you must 1st have the epub locally
- To download epubs from gutenburg project use `epub_downloader.py` 
  - To download an indiviudal book: `python3 epub_downloader.py --id 123`
  - To download collection: `python3 epub_downloader.py --all --max 10`
  - To download a random collection: `python3 epub_downloader.py --random --max 10`
  - Note: if you do not specify an output argument `--output PATH`, epubs will be downloaded to `./epubs/` 
  - For more info run `python3 epub_downloader.py --help`
- private books can also be published to the DB
- To add the book into the db use `process.py`
  - To process an individual book: `python3 process.py --input-path ./epubs/pg-123.epub`
  - To process an entire directory: `python3 process.py --input-dir ./epubs/`
  - For more info run `python3 process.py --help`
