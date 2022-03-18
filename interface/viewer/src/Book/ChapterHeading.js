import { useState } from "react"

let ChapterHeading = (props) => {
  let chapters = props.chapters
  let chapterHeading = props.chapterContent.title
  let [open, setOpen] = useState(false)
  return (
    <div className="row">
      <div className="col-md-8 offset-md-2">
        <div
          className="chapter-heading"
        >
          <div className="chapter-heading__title">{chapterHeading}</div>
        </div>
      </div>
    </div>
  )
}

export default ChapterHeading
