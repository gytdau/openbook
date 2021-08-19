var express = require("express")
var router = express.Router()
var db = require("better-sqlite3")("database.sqlite3")

router.get("/search", function (req, res, next) {})

router.get("/get/:title", function (req, res, next) {
  const book = db
    .prepare(
      `SELECT * FROM books 
    WHERE slug = (?)`
    )
    .get(req.params.title)
  const chapters = db
    .prepare(
      `SELECT * FROM chapters 
    WHERE book_id = (?)`
    )
    .all(book.id)

  book.chapters = chapters
  res.json(book)
  return
})

module.exports = router
