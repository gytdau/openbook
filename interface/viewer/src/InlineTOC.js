let InlineTOC = (props) => {
  return (
    <div className="inline-toc">
      <ol>
        {props.chapters.map((chapter) => (
          <li>
            <a href="#">{chapter.title}</a>
          </li>
        ))}
      </ol>
    </div>
  )
}
export default InlineTOC
