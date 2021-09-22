const express = require('express');

const router = express.Router();
const { Pool } = require('pg');

const pool = new Pool();

router.get('/get/:title', (req, res, next) => {
  pool.query(
    'SELECT books.*, json_agg(chapters.* ORDER BY chapters.chapter_order) as chapters FROM books LEFT JOIN chapters on books.id=chapters.book_id WHERE books.slug = $1 GROUP BY books.id',
    [req.params.title],
    (err, result) => {
      if(err)
      {
        console.log(err);
        res.status(500);
        return;
      }
      else if(result.rowCount == 0)
      {
        res.status(404);
        return;
      }
      const book = result.rows[0];
      res.json(book);
    },
  );
});

router.get('/image/:fileLocation', (req, res, next) => {
  pool.query(
    'SELECT content, format FROM images WHERE location = $1',
    [req.params.fileLocation],
    (err, result) => {
      const image = result.rows[0];
      res.contentType(`image/${image.format}`);
      res.end(image.content);
    },
  );
});

router.get('/chapter/:id', (req, res, next) => {
  pool.query(
    'SELECT * FROM chapters WHERE id = $1',
    [req.params.id],
    (err, result) => {
      const chapter = result.rows[0];
      res.json(chapter);
    },
  );
});

router.get('/catalog', (req, res, next) => {
  pool.query('SELECT * FROM books', (err, result) => {
    const books = result.rows;
    res.json(books);
  });
});

router.get('/search/:query', (req, res, next) => {
  pool.query(
    "SELECT books.id, books.title, books.author, books.slug, books.description, LEFT(chapters.content_stripped, 500) AS sample FROM books LEFT JOIN chapters ON books.id = chapters.book_id WHERE books.title LIKE ('%' || ($1) || '%')  AND chapters.chapter_order = 2",
    [req.params.query],
    (err, result) => {
      const books = result.rows;
      res.json(books);
    },
  );
});

router.get('/random', (req, res, next) => {
  // we're making the assumption that 1st image is the cover, which isnt correct, we need to find a better to solve this.
  pool.query(
    "SELECT tmp.*, images_tmp.location AS cover FROM (SELECT books.id, books.title, books.author, books.slug, books.publication FROM books order by random() LIMIT 6) AS tmp LEFT JOIN (SELECT DISTINCT ON (images.book_id) book_id, location from images) as images_tmp ON tmp.id = images_tmp.book_id;",
    [],
    (err, result) => {
      console.log(err)
      const books = result.rows;
      res.json(books);
    },
  );
});
module.exports = router;
