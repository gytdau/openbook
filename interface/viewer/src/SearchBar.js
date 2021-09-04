import { useEffect, useState } from "react"
import { useHistory, useParams } from "react-router-dom"

function SearchBar() {
  let [query, setQuery] = useState("")
  let { search } = useParams()
  useEffect(() => {
    if (search) {
      setQuery(search)
    }
  }, [search, setQuery])
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
