import logo from "./logo.svg"
import "./App.scss"
import InlineTOC from "./InlineTOC"
import ChapterHeading from "./ChapterHeading"
import ChapterView from "./ChapterView"

function BookView(props) {
  let book = props.book
  return (
    <div className="App">
      <nav class="navbar navbar-expand-md mb-4">
        <div class="container-fluid">
          <div class="collapse navbar-collapse" id="navbarCollapse">
            <ul class="navbar-nav me-auto mb-2 mb-md-0">
              <li className="nav-item">
                <i className="mdi mdi-chevron-left"></i>
              </li>
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
      <main class="container">
        <div className="row">
          <div className="col-md-8 offset-md-2">
            <div class="title-well">
              <h1 class="title-well__title">{book.title}</h1>
              <div class="title-well__details">
                <div class="detail">by {book.author}</div>
                <div class="detail">Published by Project Gutenberg</div>
              </div>
            </div>
          </div>
        </div>
      </main>
      <ChapterView chapterId={props.chapterId} book={book} />
    </div>
  )
}

export default BookView
