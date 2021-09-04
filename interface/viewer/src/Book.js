import logo from "./logo.svg"
import "./App.scss"
import InlineTOC from "./InlineTOC"
import ChapterHeading from "./ChapterHeading"
import axios from "axios"
import { useEffect, useState } from "react"
import BookView from "./BookView"
import { Redirect, useParams } from "react-router-dom"

function Book() {
  let { slug, chapterSlug } = useParams()

  let [book, setBook] = useState(null)

  useEffect(() => {
    axios.get(`/api/books/get/${slug}`).then((value) => {
      setBook(value.data)
    })
  }, [slug, setBook])

  if (book == null) {
    return <p>Loading</p>
  }
  if (chapterSlug == null) {
    return <Redirect to={`${slug}/${book.chapters[0].slug}`} />
  }
  return <BookView book={book} chapterSlug={chapterSlug} />
}

export default Book
