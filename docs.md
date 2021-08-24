# openbook

Public domain books in a better reading experience.

## Running

```
npm install
npm run build
npm start
```

## Updating the database in production

This is going to be quite a ride.

1. First, you must get postgres working on your computer. Good luck on this one.
2. Open the sqlite3 db and export to a .sql file.
3. Ensure you have a db called `openbook` for our purposes in psql
4. Take the .sql file and feed it in to postgres: `psql -d openbook -h 127.0.0.1 -U postgres < /media/gytdau/Filestore/Projects/ebook/interface/service/db.sql `
5. Open your postgres browser and dump that database, `openbook`, to a dump file
6. Upload that dump file to an S3 bucket
7. Follow these steps https://devcenter.heroku.com/articles/heroku-postgres-import-export#import-to-heroku-postgres
