import axios from "axios";
import { useEffect, useState } from "react";
import { Link, Redirect, useParams } from "react-router-dom";

function Recommendations() {
  let [recommendations, setRecommendations] = useState(null);

  useEffect(() => {
    axios.get(`/api/books/homepage_recommendations`).then((value) => {
      setRecommendations(value.data);
    });
  }, [setRecommendations]);

  if (recommendations == null) {
    return null;
  }
  return (
    <div class="recommendations">
      <div class="top">
        <div className="recommendations-section-title">Most Read</div>
        <div className="top-content">
          {recommendations.top.map((book, index) => (
            <Link to={`/${book.slug}`} className="top-book">
              <div className="top-book__number">{index + 1}.</div>
              <div className="top-book__title">
                <h2>{book.author}</h2>
                <h1>{book.title}</h1>
              </div>
            </Link>
          ))}
        </div>
      </div>

      <div class="lists">
        <div className="recommendations-section-title">
          Top 5 Books
        </div>
        <div className="lists-content">
          {recommendations.lists.map((list) => (
            <div className="list">
              <div className="list__title">
                {list.title}
              </div>
              {list.contents.map((result) => (
                <Link to={`/${result.slug}`} className="list-book">
                    <div className="list-book__title">{result.title}</div>
                </Link>
              ))}
            </div>
          ))}
        </div>
      </div>
      <div class="trending">
        <div className="recommendations-section-title">Explore the Harvard Classics</div>
        {recommendations.recent.map((result) => (
          <Link to={`/${result.slug}`} className="search-result">
            <div className="sample">
              <div className="fadeout"> </div>
              <span> {result.sample} </span>
            </div>
            <div>
              <h2>{result.title}</h2>
              <span>{result.author}</span>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}

export default Recommendations;
