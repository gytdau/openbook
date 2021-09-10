var express = require("express")
var router = express.Router()
var { Client, Pool } = require("pg")

var pool = new Pool()

router.get("/get/:title", function (req, res, next) {
  pool.query(
    `SELECT * FROM books WHERE slug = $1`,
    [req.params.title],
    (err, result) => {
      const book = result.rows[0]
      pool.query(
        `SELECT id, book_id, title, slug FROM chapters WHERE book_id = $1`,
        [book.id],
        (err, result) => {
          const chapters = result.rows
          book.chapters = chapters
          res.json(book)
        }
      )
    }
  )
})

router.get("/image/:bookId/:location", function (req, res, next) {
      pool.query(
        `SELECT content FROM images WHERE book_id = $1 AND location = $2`,
        [req.params.bookId, req.params.location],
        (err, result) => {
            res.contentType("image/png")
          const image = result.rows[0]
          res.end(image.content)
        }
      )
})

router.get("/chapter/:id", function (req, res, next) {
  pool.query(
    `SELECT * FROM chapters WHERE id = $1`,
    [req.params.id],
    (err, result) => {
      const chapter = result.rows[0]
      res.json(chapter)
    }
  )
})

router.get("/catalog", function (req, res, next) {
  pool.query("SELECT * FROM books", (err, result) => {
    const books = result.rows
    res.json(books)
  })
})

router.get("/search/:query", function (req, res, next) {
  pool.query(
    `SELECT * FROM books WHERE title LIKE ('%' || ($1) || '%')`,
    [req.params.query],
    (err, result) => {
      const books = result.rows
      res.json(books)
    }
  )
})
module.exports = router
