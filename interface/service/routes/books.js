var express = require("express")
var router = express.Router()
var { Client, Pool } = require("pg")

if (process.env.DATABASE) {
  var pool = new Pool(process.env.DATABASE)
} else {
  var pool = new Pool()
}

router.get("/get/:title", function (req, res, next) {
  pool.query(
    `SELECT * FROM books WHERE slug = $1`,
    [req.params.title],
    (err, res) => {
      const book = res.rows[0]
      pool.query(
        `SELECT * FROM chapters WHERE book_id = $1`,
        [req.params.query],
        (err, res) => {
          const chapters = res.rows
          book.chapters = chapters
          res.json(book)
        }
      )
    }
  )
})

router.get("/catalog", function (req, res, next) {
  pool.query("SELECT * FROM books", (err, res) => {
    const books = res.rows
    res.json(books)
  })
})

router.get("/search/:query", function (req, res, next) {
  pool.query(
    `SELECT * FROM books WHERE title LIKE ('%' || ($1) || '%')`,
    [req.params.query],
    (err, res) => {
      const books = res.rows
      res.json(books)
    }
  )
})
module.exports = router
