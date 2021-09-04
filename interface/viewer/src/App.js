import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom"
import "./App.scss"
import Book from "./Book"
import BookView from "./BookView"
import axios from "axios"
import Catalog from "./Catalog"
import Search from "./Search"
import Home from "./Home"

function App() {
  return (
    <Router>
      <Switch>
        <Route path="/" exact>
          <Home />
        </Route>
        <Route path="/search/:query" exact>
          <Search />
        </Route>
        <Route path="/catalog">
          <Catalog />
        </Route>
        <Route path="/:slug/:chapterSlug">
          <Book />
        </Route>
        <Route path="/:slug">
          <Book />
        </Route>
      </Switch>
    </Router>
  )
}

export default App
