import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  useHistory,
  useParams,
} from "react-router-dom"
import "./App.scss"
import Book from "./Book"
import BookView from "./BookView"
import axios from "axios"
import Catalog from "./Catalog"
import { useEffect, useState } from "react"

function SearchBar() {
  let [searchString, setSearchString] = useState("")
  let { search } = useParams()
  useEffect(() => {
    if (search) {
      setSearchString(search)
    }
  }, [search, setSearchString])
  const history = useHistory()

  return (
    <div className="search">
      <form>
        <div class="input-group border-secondary">
          <span class="input-group-prepend">
            <button class="btn ms-n3" type="button">
              <i class="mdi mdi-magnify"></i>
            </button>
          </span>
          <input
            value={searchString}
            onChange={(event) => {
              setSearchString(event.target.value)
            }}
            onKeyPress={(event) => {
              if (event.key == "Enter") {
                history.push(`/search/${searchString}`)
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
