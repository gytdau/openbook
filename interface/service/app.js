var createError = require("http-errors")
var express = require("express")
var path = require("path")
var cookieParser = require("cookie-parser")
var logger = require("morgan")
var cors = require("cors")
require("dotenv").config()

var booksRouter = require("./routes/books")

var app = express()

app.use(cors())
app.use(logger("dev"))
app.use(express.json())
app.use(express.urlencoded({ extended: false }))
app.use(cookieParser())
app.use(express.static(path.join(__dirname, "public")))

app.use("/api/books", booksRouter)

// serve our React app
app.use(express.static(path.join(__dirname, "build")))

// catch 404 and forward to error handler
app.use(function (req, res, next) {
  next(createError(404))
})

app.get("*", (req, res) => res.sendFile(resolve("build", "index.html")))

// error handler
app.use(function (err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message
  // res.locals.error = req.app.get("env") === "development" ? err : {}
  res.locals.error = err

  // render the error page
  res.status(err.status || 500)
  res.json(JSON.stringify(res.locals.message))
})

module.exports = app
