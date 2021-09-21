import { useState } from "react"
import { useHistory } from "react-router-dom"

function SearchBar(props) {
  let [query, setQuery] = useState(props.query)
  const history = useHistory()

  return (
    <div className="search-bar">
      <form>
        <div class="input-group border-secondary">
          <span class="input-group-prepend">
            <button class="btn ms-n3" type="button">
              <i class="mdi mdi-magnify"></i>
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
            class="form-control border-0"
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
