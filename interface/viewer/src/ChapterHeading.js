import { useState } from "react"
import InlineTOC from "./InlineTOC"

let ChapterHeading = (props) => {
  let chapters = props.chapters
  console.log("Chapters", chapters)
  let chapterHeading = props.chapterContent.title
  let [open, setOpen] = useState(false)
  let chevron = open ? "mdi mdi-chevron-up" : "mdi mdi-chevron-down"
  return (
    <div className="row">
      <div className="col-md-8 offset-md-2">
        <div
          className="chapter-heading"
          onClick={() => {
            setOpen(!open)
          }}
        >
          <div className="chapter-heading__title">{chapterHeading}</div>
          <div className="chapter-heading__chevron">
            <i className={chevron}></i>
          </div>
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
