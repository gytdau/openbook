import SearchBar from "./SearchBar"
import RandomBooks from "./RandomBooks"


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
      <RandomBooks />
    </>
  )
}

export default Home
