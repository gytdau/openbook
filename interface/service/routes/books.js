const express = require('express');

const router = express.Router();
const { Pool } = require('pg');

const pool = new Pool();

router.get('/get/:title', (req, res, next) => {
  pool.query(
    'SELECT * FROM books WHERE slug = $1',
    [req.params.title],
    (err, result) => {
      const book = result.rows[0];
      pool.query(
        'SELECT id, book_id, title, slug, chapter_order FROM chapters WHERE book_id = $1 ORDER BY chapter_order',
        [book.id],
        (err, result) => {
          const chapters = result.rows;
          book.chapters = chapters;
          res.json(book);
        },
      );
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
module.exports = router;
