import axios from "axios"
import { useEffect, useState } from "react"
import { Redirect, useParams } from "react-router-dom"
import BookView from "./BookView"

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
