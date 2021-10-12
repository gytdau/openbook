import { BrowserRouter as Router, Route, Switch } from "react-router-dom"
import "./App.scss"
import "./Recommendations.scss"
import Book from "./Book"
import Catalog from "./Catalog"
import Home from "./Home"
import Search from "./Search"
import BookSearch from "./BookSearch"

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
        <Route path="/book-search/:bookSlug/:query/" exact>
          <BookSearch />
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
