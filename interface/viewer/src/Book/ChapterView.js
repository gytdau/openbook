import axios from "axios";
import { useEffect, useState } from "react";
import ChapterHeading from "./ChapterHeading";
import { InView } from "react-intersection-observer";

function ChapterView(props) {
  let chapter = props.chapter;
  let chapters = props.book.chapters;
  let [chapterContent, setChapterContent] = useState(null);

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
