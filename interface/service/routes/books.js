const express = require('express');

const router = express.Router();
const { Pool } = require('pg');

const pool = new Pool();

router.get('/get/:title', async (req, res, next) => {
  try {
    const books = await pool.query(
      'SELECT books.*, json_agg(chapters.* ORDER BY chapters.chapter_order) as chapters FROM books LEFT JOIN chapters on books.id=chapters.book_id WHERE books.slug = $1 GROUP BY books.id',
      [req.params.title],
    );
    if (books.rows.length == 0) {
      res.sendStatus(404);
      return;
    }
    const book = books.rows[0];
    res.json(book);
  } catch {
    res.sendStatus(400);
  }
});

router.get('/image/:fileLocation', async (req, res, next) => {
  try {
    const result = await pool.query(
      'SELECT content, format FROM images WHERE location = $1',
      [req.params.fileLocation],
    );
    if (result.rows.length == 0) {
      res.sendStatus(404);
      return;
    }
    const image = result.rows[0];
    res.contentType(`image/${image.format}`);
    res.end(image.content);
  } catch {
    res.sendStatus(400);
  }
});

router.get('/chapter/:id', async (req, res, next) => {
  try {
    const result = await pool.query(
      'SELECT * FROM chapters WHERE id = $1',
      [req.params.id],
    );
    const chapter = result.rows[0];
    res.json(chapter);
  } catch {
    res.sendStatus(400);
  }
});

router.get('/catalog', async (req, res, next) => {
  try {
    const result = await pool.query('SELECT * FROM books');
    const books = result.rows;
    res.json(books);
  } catch {
    res.sendStatus(400);
  }
});

router.get('/search/:query', async (req, res, next) => {
  try {
    const result = await pool.query(
      `
SELECT books.id,
       books.title,
       books.author,
       books.slug,
       books.description,
       LEFT(chapters.content_stripped, 500) AS sample
FROM   books
       LEFT JOIN chapters
              ON books.id = chapters.book_id
WHERE  books.title LIKE ( '%' || ( $1 ) || '%' )
       AND chapters.chapter_order = 2`,
      [req.params.query],
    );
    const books = result.rows;
    res.json(books);
  } catch {
    res.sendStatus(400);
  }
});

router.get('/random', async (req, res, next) => {
  // we're making the assumption that 1st image is the cover, which isnt correct, we need to find a better to solve this.
  try {
    const result = await pool.query(
      `
SELECT tmp.*,
       images_tmp.location AS cover
FROM
  (SELECT books.id,
          books.title,
          books.author,
          books.slug,
          books.publication
   FROM books
   ORDER BY random()
   LIMIT 6) AS tmp
LEFT JOIN
  (SELECT DISTINCT ON (images.book_id) book_id,
                      LOCATION
   FROM images) AS images_tmp ON tmp.id = images_tmp.book_id;`,
    );
    const books = result.rows;
    res.json(books);
  } catch {
    res.sendStatus(400);
  }
});
module.exports = router;
