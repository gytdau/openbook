import { useState } from "react";
import { useHistory } from "react-router-dom";

function SearchBar(props) {
  let [query, setQuery] = useState(props.query);
  let [searchUrl, _] = useState(props.searchUrl);
  const history = useHistory();
  const submit = () => {
    if(!query) {
      alert("Type in a search query to continue.")
      return
    }
    history.push(`/${searchUrl}/${query}`);
  };

  return (
    <div className={ props.parentClassName  ? props.parentClassName : "search-bar" }>
      <form>
        <div className="input-group border-secondary">
          <input
            value={query}
            onChange={(event) => {
              setQuery(event.target.value);
            }}
            onKeyPress={(event) => {
              if (event.key == "Enter") {
                submit()
                event.preventDefault();
              }
            }}
            className= { props.inputClassName  ? props.inputClassName : "form-control border-0" }
            type="text"
            placeholder={ props.placeholder  ? props.placeholder : "Search books" }
            id="example-search-input"
          />
          <span className="input-group-append">
            <button onClick={submit} className="btn btn-primary" type="button">
              <i className="mdi mdi-magnify"></i>
            </button>
          </span>
        </div>
      </form>
    </div>
  );
}

export default SearchBar;
