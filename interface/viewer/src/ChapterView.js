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
  let location = chapters[chapterId].location
  useEffect(() => {
    setChapterContent(null)
    axios.get(`/output/${location}`).then((response) => {
      console.log(response.data)
      setChapterContent(response.data)
    })
  }, [location, setChapterContent])
  return (
    <div className="container">
      <ChapterHeading
        chapterId={chapterId}
        chapters={chapters}
        slug={props.book.slug}
      />
      <div className="row">
        <div
          className="col-md-8 offset-md-2 calibre"
          dangerouslySetInnerHTML={{ __html: chapterContent }}
        />
      </div>
    </div>
  )
}

export default ChapterView
