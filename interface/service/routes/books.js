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

router.get('/get/:title/simple', async (req, res, next) => {
  try {
    const books = await pool.query(
      'SELECT * FROM books WHERE slug = $1',
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

router.get('/chapter/:book_id/paragraphs/count', async (req, res, next) => {
  try {
    const result = await pool.query(`select paragraphs.chapters_id, chapters.chapter_order, CAST(count(paragraphs.*) as integer) from paragraphs
      LEFT JOIN chapters ON chapters.id = paragraphs.chapters_id WHERE chapters.book_id = $1 group by chapters_id, chapter_order`, [
      req.params.book_id,
    ]);
    const chapter = result.rows;
    res.json(chapter);
  } catch (error) {
    process.stdout.write(error + '\n');
    res.sendStatus(400);
  }
});


router.get('/chapter/:book_id/paragraphs', async (req, res, next) => {
  try {
    const result = await pool.query(`SELECT paragraphs.id, paragraph_order, paragraphs.chapters_id, chapter_order, book_id, title, slug, paragraphs.content FROM paragraphs
      LEFT JOIN chapters ON chapters.id = paragraphs.chapters_id WHERE chapters.book_id = $1  order by chapter_order, paragraph_order`, [
      req.params.book_id,
    ]);
    const chapter = result.rows;
    res.json(chapter);
  } catch (error) {
    process.stdout.write(error + '\n');
    res.sendStatus(400);
  }
});

router.get('/chapter/:id', async (req, res, next) => {
  try {
    const result = await pool.query('SELECT * FROM chapters WHERE id = $1', [
      req.params.id,
    ]);
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
WHERE 
      (
        to_tsvector('english', coalesce(books.title, '')) || 
        to_tsvector('english', coalesce(books.author, ''))
      ) @@ plainto_tsquery('english', $1)
       AND chapters.chapter_order = 2
LIMIT
      250`,
      [req.params.query],
    );
    const books = result.rows;
    res.json(books);
  } catch {
    res.sendStatus(400);
  }
});

let mapIntoNames = (sources) => sources.map((source) => `pg${source}-images.epub`);

router.get('/homepage_recommendations', async (req, res, next) => {
  try {
    const query = `
SELECT 
  books.id, 
  books.title, 
  books.author, 
  books.slug, 
  books.publication,
  books.ebook_source_id
FROM 
  ebook_source
  JOIN books ON books.ebook_source_id = ebook_source.id
WHERE
  ebook_source.source_id = ANY($1)
`;
    const lists = [
      {
        title: 'Classical Antiquity',
        contents: [6130, 1727, 3296, 1974, 7700],
      },
      {
        title: 'Science Fiction',
        contents: [1250, 36, 35, 29720, 21279],
      },
      {
        title: 'Religion',
        contents: [3296, 131, 398, 1653, 1549],
      },
    ];
    let top = [1342, 84, 11, 1661, 2701, 469];
    let recent = [
      1342, 1232, 1727, 2554, 3207, 20203, 996, 41, 766, 3296, 1399, 2680, 779,
      16643,
    ];

    for (let i = 0; i < lists.length; i += 1) {
      const list = lists[i];
      const result = await pool.query(query, [mapIntoNames(list.contents)]);
      list.contents = result.rows;
    }
    let result = await pool.query(query, [mapIntoNames(top)]);
    top = result.rows;
    result = await pool.query(query, [mapIntoNames(recent)]);
    recent = result.rows;
    const books = { top, recent, lists };
    res.json(books);
  } catch {
    res.sendStatus(400);
  }
});
module.exports = router;
