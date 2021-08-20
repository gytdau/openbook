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
import SearchBar from "./SearchBar"

function Home() {
  return (
    <>
      <div className="container-fluid hero">
        <div className="container">
          <div className="row">
            <div className="col-md-12">
              <h1>Great ideas</h1>
              <h2>Read free books in the public domain.</h2>
            </div>
          </div>
        </div>
      </div>
      <div className="container">
        <div className="row">
          <SearchBar />
        </div>
      </div>
    </>
  )
}

export default Home
