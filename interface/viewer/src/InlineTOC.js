import { Link } from "react-router-dom"

let InlineTOC = (props) => {
  return (
    <div className="inline-toc">
      <ol>
        {props.chapters.map((chapter, index) => (
          <li>
            <Link
              to={`/${props.slug}/${chapter.id}/${chapter.slug}`}
              onClick={() => {
                props.close()
              }}
            >
              {chapter.title}
            </Link>
          </li>
        ))}
      </ol>
    </div>
  )
}
export default InlineTOC
