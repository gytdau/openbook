import { Link } from "react-router-dom";

let BookNavbar = (props) => { 
  if(!props.visible) {
    return null;
  }
  return (
  <nav class="navbar navbar-expand mb-4">
    <div class="container-fluid">
      <div class="collapse navbar-collapse" id="navbarCollapse">
        <ul class="navbar-nav me-auto">
          <Link to="/" className="nav-item back-button d-none d-md-block">
            <i className="mdi mdi-chevron-left"></i>
          </Link>
          <li class="nav-item book-title">
            <span>{props.book.title}</span>
          </li>
          <li class="nav-item chapter-title" onClick={props.openToc}>
            <div className="nav-link">
              <span>{props.chapter ? props.chapter.title : "..."}</span>
              <span>
                <i className="mdi mdi-chevron-down"></i>
              </span>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </nav>)
};
export default BookNavbar;
