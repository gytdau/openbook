import logo from "./logo.svg"
import "./App.scss"
import InlineTOC from "./InlineTOC"
import ChapterHeading from "./ChapterHeading"
import axios from "axios"
import { useEffect, useState } from "react"
import BookView from "./BookView"
import { Redirect, useParams } from "react-router-dom"

function Book() {
  let { slug, chapterId } = useParams()

  let [book, setBook] = useState(null)

  useEffect(() => {
    axios.get(`/books/get/${slug}`).then((value) => {
      setBook(value.data)
    })
  }, [slug, setBook])

  if (book == null) {
    return <p>Loading</p>
  } else {
    if (chapterId == null) {
      return <Redirect to={`${slug}/1/test`} />
    }
    return <BookView book={book} chapterId={chapterId} />
  }
}

export default Book
