import axios from "axios"
import { useEffect, useState } from "react"
import ChapterHeading from "./ChapterHeading"

function ChapterView(props) {
  let chapter = props.chapter
  let chapters = props.book.chapters
  let [chapterContent, setChapterContent] = useState(null)
  useEffect(() => {
    setChapterContent(null)
    axios.get(`/api/books/chapter/${chapter.id}`).then((response) => {
      console.log(response.data)
      setChapterContent(response.data)
    })
  }, [chapter, setChapterContent])
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
