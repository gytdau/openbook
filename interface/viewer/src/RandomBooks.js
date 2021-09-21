import axios from "axios"
import { useEffect, useState } from "react"
import { Link } from "react-router-dom"

function RandomBooks() {
    const [books, setBooks] = useState([]);
    useEffect(() => {
        axios.get(`/api/books/random`).then((res) => {
            console.log(res)
            setBooks(res.data)
        })
      }, [setBooks])


  return (
    <div className="books-view container">
        <div id="display" className="row row-eq-height justify-content-center m-3">
            <div className="row row-cols-1 row-cols-sm-2 row-cols-md-4 row-cols-lg-5 g-4 text-center">
            {books != null && books.map((book) => 
                <Link to={`/${book.slug}`} className="col no_dec">
                    <div className="card h-100">
                        <img className="card-img-top" alt={book.title} src={`api/books/image/${book.cover}`} />
                        <div className="card-body card-body-flex">
                            <div className="card-title w-100">
                                <p>{book.title}</p>
                                <p className="text-muted">{book.author}</p>
                            </div>

                        </div>
                        <div className="card-footer text-muted">Published Date</div>
                    </div>
                </Link>
            )}
            </div>
        </div>
    </div>
  )
}

export default RandomBooks
