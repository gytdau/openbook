import { Link, NavLink } from 'react-router-dom';
import Modal from 'react-modal';
import { useEffect } from 'react';

const TOC = (props) => {
  useEffect(() => {
    document.body.style.overflow = props.open ? 'hidden' : 'unset';
  }, [props.open]);
  return (
    <Modal isOpen={props.open} className="modal d-block" shouldCloseOnOverlayClick onRequestClose={props.close}>
      <div className="modal-dialog modal-lg modal-toc">

        <div className="modal-content">
          <div className="modal-header">
            Table of Contents

            <div className="btn btn-close" data-testid="close-toc" onClick={props.close} />
          </div>

          <div className="modal-body m-0">
            <div className="list-group list-group-flush">
              {props.chapters.map((chapter, index) => (
                <Link
                  to={`/${props.slug}/${chapter.slug}`}
                  onClick={() => {
                    props.close();
                    window.scroll({
                      top: 0,
                      behavior: 'auto',
                    });
                    props.clearVisibleChapters(chapter);
                  }}
                  className="list-group-item list-group-item-action"
                  exact
                >
                  {chapter.title}
                </Link>
              ))}
            </div>
          </div>
        </div>
      </div>
    </Modal>
  );
};
export default TOC;
