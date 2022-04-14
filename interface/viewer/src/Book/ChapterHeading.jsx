import { useState } from 'react';
import { Link } from 'react-router-dom';

const ChapterHeading = (props) => {
  const { chapters } = props;
  const chapterHeading = props.chapterContent.title;
  const [open, setOpen] = useState(false);
  return (
    <div className="row">
      <div className="col-md-8 offset-md-2">
        <div
          className="chapter-subheading"
        >
          <div className="chapter-heading__title">{chapterHeading}</div>
        </div>
        <div className="chapter-subheading"><Link to={`/immersive/${props.slug}/${props.chapterContent.slug}`}>Start Immersive Mode</Link></div>
      </div>
    </div>
  );
};

export default ChapterHeading;
