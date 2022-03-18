import './SimpleView.scss';
import { useEffect, useState, useReducer } from 'react';
import { Link, useParams } from 'react-router-dom';
import axios from 'axios';
import BookNavbar from '../Book/BookNavbar';

function getFirstChapter(chapters) {
  let keys = Object.keys(chapters);
  keys = keys.filter((value, index, arr) => value[0]);
  const counts = new Uint32Array(keys.map(Number)).sort();
  const chapter = counts[0];
  const paragraph = chapters[chapter];
  return [chapter, paragraph];
}

function getLastChapter(chapters) {
  let keys = Object.keys(chapters);
  keys = keys.filter((value, index, arr) => value.length < 4);
  const counts = new Uint32Array(keys.map(Number)).sort();
  const chapter = counts.reverse()[0];
  const paragraph = chapters[chapter];
  return [chapter, paragraph];
}

function SimpleView(props) {
  const { slug, chapterSlug } = useParams();

  const [book, setBook] = useState(null);
  const [activeChapter, updateActiveChapter] = useReducer(activeChapterReducer, {
    chapter: 1, paragraph: 1, chapters: [], action: 1,
  });
  const [paragraphs, setParagraphs] = useState([]);

  function activeChapterReducer(state, action) {
    console.log(state, action);
    switch (action.type) {
      case 'next':

        if (state.paragraph + 1 < state.chapters[state.chapter]) return { ...state, paragraph: state.paragraph + 1, action: 1 };
        if (state.chapter + 1 < state.chapters.length) {
          return {
            ...state, paragraph: 1, chapter: state.chapter + 1, action: 1,
          };
        }
        break;

      case 'previous':

        if (state.paragraph - 1 >= 0) return { ...state, paragraph: state.paragraph - 1, action: -1 };
        if (state.chapter - 1 >= 0) {
          return {
            ...state, paragraph: state.chapters[state.chapter - 1] - 1, chapter: state.chapter - 1, action: -1,
          };
        }
        break;

      case 'reset':
        return {
          chapter: 1, paragraph: 1, chapters: [], action: 1,
        };

      case 'restart':
        const chapter = getFirstChapter(state.chapters)[0];
        return {
          ...state, chapter, paragraph: 1, action: 1,
        };
      case 'update':
        return { ...state, chapters: action.chapters };
      default:
        throw new Error();
    }
    return { ...state };
  }

  function repeatAction() {
    if (activeChapter.action == 1) {
      updateActiveChapter({ type: 'next' });
    } else {
      updateActiveChapter({ type: 'previous' });
    }
  }

  function getActiveParagraph() {
    if (activeChapter.chapters.length == 0) {
      return;
    }

    // console.log("Pre-getActiveParagraph", activeChapter);
    if (!(activeChapter.chapter in activeChapter.chapters)) {
      const lastChapter = getLastChapter(activeChapter.chapters)[0];
      if (lastChapter > activeChapter.chapter) {
        repeatAction();
      } else {
        updateActiveChapter({ type: 'restart' });
      }
      return;
    }
    // console.log("Post-getActiveParagraph", activeChapter);

    if (!(activeChapter.paragraph in paragraphs[activeChapter.chapter])) {
      repeatAction();
      return;
    }

    return paragraphs[activeChapter.chapter][activeChapter.paragraph].content;
  }

  useEffect(() => {
    axios.get(`/api/books/get/${slug}/simple`)
      .then((value) => value.data)
      .then((book) => {
        setBook(book);
        console.log(book);

        return book;
      })
      .then((book) => {
        updateActiveChapter({ type: 'reset' });

        setParagraphs((prevState) => []);
        axios.get(`/api/books/chapter/${book.id}/paragraphs`)
          .then((value) => value.data)
          .then((data) => {
            // console.log("data", data)
            const map = {};

            for (let i = 0; i < data.length; i++) {
              const tmp = data[i];
              if (!(tmp.chapter_order in map)) {
                map[tmp.chapter_order] = {};
              }
              map[tmp.chapter_order][tmp.paragraph_order] = tmp;
            }
            // console.log("MAP", map)
            setParagraphs(map);
            axios.get(`/api/books/chapter/${book.id}/paragraphs/count`)
              .then((value) => value.data)
              .then((limits) => {
                // console.log("limits", limits);
                const limits_map = Object.assign({}, ...limits.map((x) => ({ [x.chapter_order]: x.count })));
                const counts = new Uint32Array(Object.keys(limits_map).map(Number)).sort();
                const last_chapter = counts.reverse()[0];
                limits_map.length = last_chapter;

                // console.log("limits_map", limits_map);
                updateActiveChapter({ type: 'update', chapters: limits_map });
                updateActiveChapter({ type: 'restart' });
              });
          });
      });
  }, [slug, setBook]);

  const keypressHandler = (e) => {
    if (e.key === 'ArrowLeft') {
      updateActiveChapter({ type: 'previous' });
    }
    if (e.key === 'ArrowRight') {
      updateActiveChapter({ type: 'next' });
    }
    console.log(e);
  };

  useEffect(() => {
    window.addEventListener('keydown', keypressHandler);

    return () => {
      window.removeEventListener('keydown', keypressHandler);
    };
  });

  if (book && activeChapter.chapters.length > 0) {
    if (book != null && activeChapter.chapter in paragraphs) {
      // var doc = new DOMParser().parseFromString(book.chapters[activeChapter.chapter].content, "text/html");
      // var text = doc.body.textContent.replaceAll("\n\n", "\n");
      // console.log("PP", activeChapter, paragraphs)
      return (
        <div className="App" id="#react-scroller">
          {/* <BookNavbar
              chapter={paragraphs[activeChapter.chapter][activeChapter.paragraph]}
              book={book}
              // openToc={() => {
              //   setTocOpen(true);
              // }}
              visible={true}
            /> */}

          <div className="flex-center position-ref full-height">
            <div className="container">
              <div className="content">
                <h3 dangerouslySetInnerHTML={{ __html: getActiveParagraph() }} />
              </div>
            </div>
          </div>
        </div>
      );
    }
  } else {
    return null;
  }
  return null;
}

export default SimpleView;
