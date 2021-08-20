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
import SearchBar from "./SearchBar"

function Search() {
  let { search } = useParams()
  let [results, setResults] = useState(null)
  useEffect(() => {
    axios.get(`/books/search/${search}`).then((res) => {
      setResults(res.data)
    })
  }, [setResults, search])
  let resultsDisplay = null
  if (results === null) {
    resultsDisplay = <p>Loading....</p>
  } else if (results.length == 0) {
    resultsDisplay = <p>No results</p>
  } else {
    resultsDisplay = results.map((result) => {
      return (
        <Link to={`/${result.slug}/0/test`} className="search-result">
          <div>
            <h2>{result.title}</h2>
            <span>{result.author}</span>
          </div>
        </Link>
      )
    })
  }
  return (
    <div className="container">
      <div className="row">
        <div className="search">
          <SearchBar />
        </div>
      </div>
      <div className="row">
        <div className="search-results">{resultsDisplay}</div>
      </div>
    </div>
  )
}

export default Search
