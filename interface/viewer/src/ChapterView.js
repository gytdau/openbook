import logo from "./logo.svg"
import "./App.scss"
import InlineTOC from "./InlineTOC"
import ChapterHeading from "./ChapterHeading"
import { useEffect, useState } from "react"
import axios from "axios"

function ChapterView(props) {
  let chapterId = props.chapterId
  let chapters = props.book.chapters
  let [chapterContent, setChapterContent] = useState(null)
  useEffect(() => {
    setChapterContent(null)
    axios.get(`/books/chapter/${chapterId}`).then((response) => {
      console.log(response.data)
      setChapterContent(response.data)
    })
  }, [chapterId, setChapterContent])
  if (!chapterContent) {
    return null
  }
  return (
    <div className="container">
      <ChapterHeading
        chapterContent={chapterContent}
        chapters={chapters}
        slug={props.book.slug}
      />
      <div className="row">
        <div
          className="col-md-8 offset-md-2 calibre"
          dangerouslySetInnerHTML={{ __html: chapterContent.content }}
        />
      </div>
    </div>
  )
}

export default ChapterView
