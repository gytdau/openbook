import { Link } from "react-router-dom"

let InlineTOC = (props) => {
  return (
    <div className="inline-toc">
      <ol>
        {props.chapters.map((chapter, index) => (
          <li>
            <Link to={`/${props.slug}/${index}/test`}>{chapter.title}</Link>
          </li>
        ))}
      </ol>
    </div>
  )
}
export default InlineTOC
