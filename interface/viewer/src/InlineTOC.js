import { Link, NavLink } from "react-router-dom"

let InlineTOC = (props) => {
  return (
    <div className="inline-toc">
      <div className="list-group list-group-flush">
        {props.chapters.map((chapter, index) => (
            <NavLink
            
              to={`/${props.slug}/${chapter.slug}`}
              onClick={() => {
                props.close()
                window.scroll({
                  top: 0,
                  behavior: 'auto' }
                  )
                props.clearVisibleChapters(chapter)
              }}
              className="list-group-item list-group-item-action"
              activeClassName="active"
              exact={true}
              
            >
              {chapter.title}
            </NavLink>
        ))}
      </div>
    </div>
  )
}
export default InlineTOC
