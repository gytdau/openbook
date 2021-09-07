import { useEffect, useState } from "react"
import InfiniteScroll from "react-infinite-scroll-component"
import { Link } from "react-router-dom"
import ChapterView from "./ChapterView"

function getChapterFromSlug(book, chapterSlug) {
  let found = book.chapters.find((chapter, index) => {
    if (chapter.slug === chapterSlug) {
      console.log("Chapter found from slug", chapter)
      return true
    }
  })
  if (found) {
    return found
  }
  return book.chapters[0]
}

function BookView(props) {
  let { book, chapterSlug } = props
  let [renderedChapters, setRenderedChapters] = useState([])

  let lastRenderedChapterIndex = book.chapters.indexOf(
    renderedChapters[renderedChapters.length - 1]
  )

  let noMoreChaptersRemaining =
    lastRenderedChapterIndex == book.chapters.length - 1
  let isHeaderHidden = book.chapters.indexOf(renderedChapters[0]) > 0

  let renderNewChapter = () => {
    let newRenderedChapters = [
      ...renderedChapters,
      book.chapters[lastRenderedChapterIndex + 1],
    ]
    setRenderedChapters(newRenderedChapters)
  }

  useEffect(() => {
    let chapters = [getChapterFromSlug(book, chapterSlug)]
    let chapter_index = book.chapters.indexOf(chapters[0])
    if (chapter_index + 1 < book.chapters.length) {
      chapters.push(book.chapters[chapter_index + 1])
    }
    if (chapter_index + 2 < book.chapters.length) {
      chapters.push(book.chapters[chapter_index + 2])
    }
    if (chapter_index + 3 < book.chapters.length) {
      chapters.push(book.chapters[chapter_index + 3])
    }
    setRenderedChapters(chapters)
  }, [book, chapterSlug])

  if (renderedChapters.length == 0) {
    return null
  }

  return (
    <div className="App" id="#react-scroller">
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
        next={renderNewChapter}
        hasMore={!noMoreChaptersRemaining}
        loader={<p>Loading...</p>}
        scrollThreshold={0.8}
        endMessage={<p>End of book</p>}
      >
        {renderedChapters.map((chapter) => (
          <ChapterView chapter={chapter} book={book} key={chapter.id} />
        ))}
      </InfiniteScroll>
    </div>
  )
}

export default BookView
