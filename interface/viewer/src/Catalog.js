import axios from "axios"
import { useEffect, useState } from "react"
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom"
import "./App.scss"
import Book from "./Book"
import BookView from "./BookView"

function Catalog() {
  let [catalog, setCatalog] = useState(null)
  useEffect(() => {
    axios.get("/api/books/catalog").then((res) => {
      setCatalog(res.data)
    })
  }, [setCatalog])
  if (!catalog) {
    return null
  }

  return (
    <div className="container">
      <div className="row">
        <div className="col-md-8 offset-2">
          {catalog.map((book) => (
            <li>
              <Link to={`/${book.slug}`}>{book.title}</Link>
            </li>
          ))}
        </div>
      </div>
    </div>
  )
}

export default Catalog
