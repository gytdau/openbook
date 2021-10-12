import { useEffect, useState } from "react";
import InfiniteScroll from "react-infinite-scroll-component";
import { Link } from "react-router-dom";
import BookNavbar from "./BookNavbar";
import ChapterView from "./ChapterView";
import TOC from "./TOC";

function getChapterFromSlug(book, chapterSlug) {
  let found = book.chapters.find((chapter, index) => {
    if (chapter.slug === chapterSlug) {
      return true;
    }
  });
  if (found) {
    return found;
  }
  return book.chapters[0];
}

function BookView(props) {
  let { book, chapterSlug } = props;
  let [renderedChapters, setRenderedChapters] = useState([]);
  let [visibleChapters, setVisibleChapters] = useState(new Set());
  let [tocOpen, setTocOpen] = useState(false);

  let orderedVisibleChapters = Array.from(visibleChapters).sort(
    (a, b) => a.chapter_order - b.chapter_order
  );
  let chapter = null;
  if (orderedVisibleChapters.length >= 1) {
    chapter = orderedVisibleChapters[0];
  }

  useEffect(() => {
    if (!chapter) {
      return;
    }
    window.history.replaceState(null, null, `/${book.slug}/${chapter.slug}`);
  }, [chapter, book.slug]);

  let lastRenderedChapterIndex = book.chapters.indexOf(
    renderedChapters[renderedChapters.length - 1]
  );

  let noMoreChaptersRemaining =
    lastRenderedChapterIndex == book.chapters.length - 1;
  let isHeaderHidden = book.chapters.indexOf(renderedChapters[0]) > 0;

  let renderNewChapter = () => {
    let newRenderedChapters = [
      ...renderedChapters,
      book.chapters[lastRenderedChapterIndex + 1],
    ];
    setRenderedChapters(newRenderedChapters);
  };

  useEffect(() => {
    let chapters = [getChapterFromSlug(book, chapterSlug)];
    let chapter_index = book.chapters.indexOf(chapters[0]);
    if (chapter_index + 1 < book.chapters.length) {
      chapters.push(book.chapters[chapter_index + 1]);
    }
    if (chapter_index + 2 < book.chapters.length) {
      chapters.push(book.chapters[chapter_index + 2]);
    }
    if (chapter_index + 3 < book.chapters.length) {
      chapters.push(book.chapters[chapter_index + 3]);
    }
    setRenderedChapters(chapters);
    setVisibleChapters(new Set());
  }, [book, chapterSlug]);

  if (renderedChapters.length == 0) {
    return null;
  }

  return (
    <div className="App" id="#react-scroller">
      <BookNavbar
        chapter={chapter}
        book={book}
        openToc={() => {
          setTocOpen(true);
        }}
      />
      <TOC
        clearVisibleChapters={(chapter) => {
          console.log("RESETTING", chapter);
          setVisibleChapters(new Set([chapter]));
        }}
        open={tocOpen}
        close={() => {
          setTocOpen(false);
        }}
        chapters={book.chapters}
        slug={book.slug}
      />
      {isHeaderHidden ? (
        <div className="container m-4 p-4"></div>
      ) : (
        <main class="container">
          <div className="row">
            <div className="col-md-8 offset-md-2">
              <div class="title-well">
                <h1 class="title-well__title">{book.title}</h1>
                <div class="title-well__details">
                  {book.author ? (
                    <div class="detail">by {book.author}</div>
                  ) : null}
                  <div class="detail">Published by Project Gutenberg</div>
                </div>
              </div>
            </div>
          </div>
        </main>
      )}
      <InfiniteScroll
        dataLength={renderedChapters.length}
        next={renderNewChapter}
        hasMore={!noMoreChaptersRemaining}
        loader={<p>Loading...</p>}
        scrollThreshold={0.8}
        endMessage={<p>End of book</p>}
      >
        {renderedChapters.map((chapter) => (
          <ChapterView
            chapter={chapter}
            book={book}
            key={chapter.id}
            onViewChange={(inView) => {
              let newVisibleChapters = new Set(visibleChapters);
              if (inView) {
                newVisibleChapters.add(chapter);
                console.log("ADDING", chapter);
              } else {
                newVisibleChapters.delete(chapter);
                console.log("DELETING", chapter);
              }
              setVisibleChapters(newVisibleChapters);
            }}
          />
        ))}
      </InfiniteScroll>
    </div>
  );
}

export default BookView;
