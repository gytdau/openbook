import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom"
import "./App.scss"
import Book from "./Book"
import BookView from "./BookView"

function App() {
  return (
    <Router>
      <Switch>
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
