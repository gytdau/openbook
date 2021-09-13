const express = require('express');
const path = require('path');
const cookieParser = require('cookie-parser');
const logger = require('morgan');
const cors = require('cors');
require('dotenv').config();

const booksRouter = require('./routes/books');

const app = express();

app.use(cors());
app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/api/books', booksRouter);

// serve our React app
app.use(express.static(path.join(__dirname, 'build')));

app.get('*', (req, res) => {
  console.log('Serve static');
  res.sendFile(path.join(__dirname, './build/index.html'));
});

// error handler
app.use((err, req, res, next) => {
  // set locals, only providing error in development
  res.locals.message = err.message;
  // res.locals.error = req.app.get("env") === "development" ? err : {}
  res.locals.error = err;

  // render the error page
  res.status(err.status || 500);
  res.json(JSON.stringify(res.locals.message));
});

module.exports = app;
