import { useState } from 'react';
import { useHistory } from 'react-router-dom';

function SearchBar(props) {
  const [query, setQuery] = useState(props.query);
  const history = useHistory();
  const submit = () => {
    if (!query) {
      alert('Type in a search query to continue.');
      return;
    }
    history.push(`/search/${query}`);
  };

  return (
    <div className="search-bar">
      <form>
        <div className="input-group border-secondary">
          <input
            value={query}
            onChange={(event) => {
              setQuery(event.target.value);
            }}
            onKeyPress={(event) => {
              if (event.key == 'Enter') {
                submit();
                event.preventDefault();
              }
            }}
            className="form-control border-0"
            type="text"
            placeholder="Search books"
            id="example-search-input"
          />
          <span className="input-group-append">
            <button onClick={submit} className="btn btn-primary" type="button">
              <i className="mdi mdi-magnify" />
            </button>
          </span>
        </div>
      </form>
    </div>
  );
}

export default SearchBar;
