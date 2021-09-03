import logo from "./logo.svg"
import InfiniteScroll from "react-infinite-scroll-component"
import "./App.scss"
import InlineTOC from "./InlineTOC"
import ChapterHeading from "./ChapterHeading"
import ChapterView from "./ChapterView"
import { Link } from "react-router-dom"
import { useEffect, useState } from "react"

function BookView(props) {
  let book = props.book
  let [renderedChapters, setRenderedChapters] = useState([
    parseInt(props.chapterId),
  ])
  useEffect(() => {
    setRenderedChapters([parseInt(props.chapterId)])
  }, [props.chapterId])

  let isHeaderHidden = parseInt(props.chapterId) != 1

  let last = renderedChapters[renderedChapters.length - 1]
  let isLast = last == props.book.chapters.length - 1
  let fetchData = () => {
    let newRenderedChapters = [...renderedChapters, last + 1]
    console.log(newRenderedChapters)
    setRenderedChapters(newRenderedChapters)
  }
  return (
    <div className="App">
      <nav class="navbar navbar-expand-md mb-4">
        <div class="container-fluid">
          <div class="collapse navbar-collapse" id="navbarCollapse">
            <ul class="navbar-nav me-auto mb-2 mb-md-0">
              <Link to="/" className="nav-item m-4">
                <i className="mdi mdi-chevron-left"></i>
              </Link>
              <li class="nav-item book-title">
                <span>{book.title}</span>
                <a class="nav-link active" aria-current="page" href="#">
                  Chapter 1 <i class="mdi mdi-chevron-down"></i>
                </a>
              </li>
            </ul>
          </div>
        </div>
      </nav>
      {isHeaderHidden ? (
        <div className="container m-4 p-4"></div>
      ) : (
        <main class="container">
          <div className="row">
            <div className="col-md-8 offset-md-2">
              <div class="title-well">
                <h1 class="title-well__title">{book.title}</h1>
                <div class="title-well__details">
                  {book.author ? (
                    <div class="detail">by {book.author}</div>
                  ) : null}
                  <div class="detail">Published by Project Gutenberg</div>
                </div>
              </div>
            </div>
          </div>
        </main>
      )}
      <InfiniteScroll
        dataLength={renderedChapters.length}
        next={fetchData}
        hasMore={!isLast}
        loader={<p>Loading...</p>}
        endMessage={<p>End of book</p>}
      >
        {renderedChapters.map((chapterId) => (
          <ChapterView chapterId={chapterId} book={book} />
        ))}
      </InfiniteScroll>
    </div>
  )
}

export default BookView
