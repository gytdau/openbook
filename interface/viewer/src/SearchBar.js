import { useState } from "react"
import { useHistory } from "react-router-dom"

function SearchBar(props) {
  let [query, setQuery] = useState(props.query)
  const history = useHistory()

  return (
    <div className="search-bar">
      <form>
        <div className="input-group border-secondary">
          <span className="input-group-prepend">
            <button className="btn ms-n3" type="button">
              <i className="mdi mdi-magnify"></i>
            </button>
          </span>
          <input
            value={query}
            onChange={(event) => {
              setQuery(event.target.value)
            }}
            onKeyPress={(event) => {
              if (event.key == "Enter") {
                history.push(`/search/${query}`)
                event.preventDefault()
              }
            }}
            className="form-control border-0"
            type="text"
            placeholder="Search books"
            id="example-search-input"
          />
        </div>
      </form>
    </div>
  )
}

export default SearchBar
