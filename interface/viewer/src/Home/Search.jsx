import axios from 'axios';
import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import SearchBar from './SearchBar';

function Search() {
  const { query } = useParams();
  const [results, setResults] = useState(null);
  useEffect(() => {
    axios.get(`/api/books/search/${query}`).then((res) => {
      setResults(res.data);
    });
  }, [setResults, query]);
  let resultsDisplay = null;
  if (results === null) {
    resultsDisplay = <p>Loading....</p>;
  } else if (results.length == 0) {
    resultsDisplay = <p>No results</p>;
  } else {
    resultsDisplay = results.map((result) => (
      <Link to={`/${result.slug}`} className="search-result">
        <div className="sample">
          <div className="fadeout"> </div>
          <span>
            {' '}
            {result.sample}
            {' '}
          </span>
        </div>
        <div>
          <h2>{result.title}</h2>
          <span>{result.author}</span>
        </div>
      </Link>
    ));
  }
  return (
    <div className="container">
      <div className="row">
        <div className="search">
          <SearchBar query={query} />
        </div>
      </div>
      <div className="row">
        <div className="search-results">{resultsDisplay}</div>
      </div>
    </div>
  );
}

export default Search;
