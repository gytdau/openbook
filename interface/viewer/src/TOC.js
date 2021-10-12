import { Link, NavLink } from "react-router-dom";
import Modal from "react-modal";

let TOC = (props) => {
  return (
    <Modal isOpen={props.open} className="modal d-block">
      <div className="modal-dialog modal-lg">
      <div className="modal-content">
        <div className="list-group list-group-flush">
          {props.chapters.map((chapter, index) => (
            <Link
              to={`/${props.slug}/${chapter.slug}`}
              onClick={() => {
                props.close();
                window.scroll({
                  top: 0,
                  behavior: "auto",
                });
                props.clearVisibleChapters(chapter);
              }}
              className="list-group-item list-group-item-action"
              exact={true}
            >
              {chapter.title}
            </Link>
          ))}
        </div>
      </div>
</div>
    </Modal>
  );
};
export default TOC;
