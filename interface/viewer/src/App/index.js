import { BrowserRouter as Router, Route, Switch } from "react-router-dom"
import "./App.scss"
import "./Recommendations.scss"
import Book from "../Book/Book"
import Catalog from "../Home/Catalog"
import Home from "../Home/Home"
import Search from "../Home/Search"
import SimpleView from "../SimpleView/SimpleView"

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
        <Route path="/immersive/:slug/:chapterSlug">
          <SimpleView />
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
