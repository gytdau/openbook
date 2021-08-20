import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  useHistory,
} from "react-router-dom"
import "./App.scss"
import Book from "./Book"
import BookView from "./BookView"
import axios from "axios"
import Catalog from "./Catalog"
import { useState } from "react"

function Home() {
  let [searchString, setSearchString] = useState("")
  const history = useHistory()

  return (
    <div className="container">
      <div className="row">
        <div className="col-md-12">
          <h1>Free public domain books</h1>
        </div>
      </div>
      <div className="row">
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
      </div>
    </div>
  )
}

export default Home
