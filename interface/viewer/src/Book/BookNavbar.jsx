import { Link } from 'react-router-dom';

const BookNavbar = (props) => {
  if (!props.visible) {
    return null;
  }
  return (
    <nav className="navbar navbar-expand mb-4">
      <div className="container-fluid">
        <div className="collapse navbar-collapse" id="navbarCollapse">
          <ul className="navbar-nav me-auto">
            <Link to="/" className="nav-item back-button d-none d-md-block">
              <i className="mdi mdi-chevron-left" />
            </Link>
            <li className="nav-item book-title">
              <span>{props.book.title}</span>
            </li>
            <li className="nav-item chapter-title" data-testid="open-toc" onClick={props.openToc}>
              <div className="nav-link">
                <span>{props.chapter ? props.chapter.title : '...'}</span>
                <span>
                  <i className="mdi mdi-chevron-down" />
                </span>
              </div>
            </li>
            {props.paragraph_order ?
            <li className="nav-item paragraph-order">
                <span>{props.paragraph_order}</span>
            </li> : null}
          </ul>
        </div>
      </div>
    </nav>
  );
};
export default BookNavbar;
