import axios from "axios"
import { useEffect, useState } from "react"
import { Link, useParams } from "react-router-dom"
import SearchBar from "../Home/SearchBar"

function BookSearch(props) {
  let { bookSlug, query } = useParams()
  let [results, setResults] = useState(null)

  useEffect(() => {
    axios.get(`/api/books/book-search/${bookSlug}/${query}`).then((res) => {
      setResults(res.data)
    })
  }, [setResults, bookSlug, query])
  let resultsDisplay = null
  if (results === null) {
    resultsDisplay = <p>Loading....</p>
  } else if (results.length == 0) {
    resultsDisplay = <p>No results</p>
  } else {
    resultsDisplay = results.map((result) => {
      return (
        <Link to={`/${bookSlug}/${result.slug}`} className="search-result">
          <div className="sample">
            <div className="fadeout"> </div>
            <span dangerouslySetInnerHTML={{ __html: result.highlights}}></span>
          </div>
          <div>
            <h2>{result.title}</h2>
          </div>
        </Link>
      )
    })
  }
  return (
    <div className="container">
      <div className="row">
        <div className="search">
          <SearchBar placeholder="Search Chapters" searchUrl={`book-search/${bookSlug}`} query={query}/>
        </div>
      </div>
      <div className="row">
        <div className="search-results">{resultsDisplay}</div>
      </div>
    </div>
  )
}

export default BookSearch
