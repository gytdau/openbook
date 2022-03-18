import axios from 'axios';
import { useEffect, useState } from 'react';
import { InView } from 'react-intersection-observer';
import ChapterHeading from './ChapterHeading';

function ChapterView(props) {
  const { chapter } = props;
  const { chapters } = props.book;
  const [chapterContent, setChapterContent] = useState(null);

  useEffect(() => {
    setChapterContent(null);
    axios.get(`/api/books/chapter/${chapter.id}`).then((response) => {
      setChapterContent(response.data);
    });
  }, [chapter, setChapterContent]);

  if (!chapterContent) {
    return null;
  }
  return (
    <div className="container">
      <InView as="div" onChange={props.onViewChange}>
        <ChapterHeading
          chapterContent={chapterContent}
          chapters={chapters}
          slug={props.book.slug}
          clearVisibleChapters={props.clearVisibleChapters}
        />
        <div className="row">
          <div
            className="col-md-8 offset-md-2 calibre"
            dangerouslySetInnerHTML={{ __html: chapterContent.content }}
          />
        </div>
      </InView>
    </div>
  );
}

export default ChapterView;
