var express = require("express")
var router = express.Router()
var sqlite = require("sqlite3")
var db = new sqlite.Database("../database.sqlite3")

router.get("/search", function (req, res, next) {})

router.get("/book/:title", function (req, res, next) {
  db.get("SELECT * FROM books WHERE title = (?)", req.title, (error, row) => {
    if (error) {
      res.send(error)
      return
    }
    res.send(row)
  })
})
module.exports = router
