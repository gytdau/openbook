import react, { useState } from "react"
import InlineTOC from "./InlineTOC"

let ChapterHeading = (props) => {
  let chapters = props.chapters
  let chapterHeading = chapters[props.chapterId].title
  let [open, setOpen] = useState(false)
  let chevron = open ? "mdi mdi-chevron-up" : "mdi mdi-chevron-down"
  return (
    <div className="row">
      <div className="col-md-8 offset-md-2">
        <div
          className="chapter"
          onClick={() => {
            setOpen(!open)
          }}
        >
          {chapterHeading} <i className={chevron}></i>
        </div>
        {open ? (
          <div className="chapter-toc">
            <InlineTOC
              chapters={chapters}
              slug={props.slug}
              close={() => {
                setOpen(false)
              }}
            />
            <div
              className="chapter-toc__close btn btn-outline-secondary"
              onClick={() => {
                setOpen(false)
              }}
            >
              Close <i className="mdi mdi-close"></i>
            </div>
          </div>
        ) : null}
      </div>
    </div>
  )
}

export default ChapterHeading
