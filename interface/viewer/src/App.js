import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom"
import "./App.scss"
import Book from "./Book"
import BookView from "./BookView"
import axios from "axios"
import Catalog from "./Catalog"

axios.defaults.baseURL = "http://localhost:5000"

function App() {
  return (
    <Router>
      <Switch>
        <Route path="/catalog">
          <Catalog />
        </Route>
        <Route path="/:slug/:chapterId/:chapterSlug">
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
