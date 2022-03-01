import "./SimpleView.scss"
import { useEffect, useState, useReducer } from "react";
import { Link, useParams } from "react-router-dom";
import BookNavbar from "./BookNavbar";
import axios from "axios";

function SimpleView(props) {

  let { slug, chapterSlug } = useParams()

  let [book, setBook] = useState(null)
  let [activeChapter, updateActiveChapter] = useReducer(activeChapterReducer, {chapter: 1, paragraph: 1, chapters: [], action: 1})
  let [paragraphs, setParagraphs] = useState([])

  function activeChapterReducer(state, action) {
    console.log(state, action)
    switch (action.type) {
      case 'next':

        if(state.paragraph + 1 < state.chapters[state.chapter])
          return {...state, paragraph: state.paragraph + 1, action: 1};
        else
          if(state.chapter + 1 < state.chapters.length)
            return {...state, paragraph: 1, chapter: state.chapter + 1, action: 1};
        break;

      case 'previous':

        if(state.paragraph - 1 >= 0)
          return {...state, paragraph: state.paragraph - 1, action: -1};
        else
          if(state.chapter - 1 >= 0)
            return {...state, paragraph: state.chapters[state.chapter - 1] - 1, chapter: state.chapter - 1, action: -1};
        break;

        case 'reset':
          return {chapter: 1, paragraph: 1, chapters: [], action: 1};

        case 'restart':
          return {...state, chapter: 1, paragraph: 1, action: 1};
      case 'update':
        return {...state, chapters: action.chapters};
      default:
        throw new Error();
    }
    return {...state};
  }

  function repeatAction()
  {
    if(activeChapter.action == 1)
    {
      updateActiveChapter({type: 'next'})
    }
    else
    {
      updateActiveChapter({type: 'previous'})
    }
  }

  function getActiveParagraph()
  {
    if(activeChapter.chapters.length == 0)
    {
      return;
    }

    // console.log("Pre-getActiveParagraph", activeChapter);
    if(!(activeChapter.chapter in activeChapter.chapters))
    {
      let counts = Object.keys(activeChapter.chapters).sort()
      if(counts.pop() > activeChapter.chapter)
      {
        repeatAction()
      }
      else
      {
        updateActiveChapter({type: 'restart'})
      }
      return;
    }
    // console.log("Post-getActiveParagraph", activeChapter);

    if(!(activeChapter.paragraph in paragraphs[activeChapter.chapter]))
    {
      repeatAction()
      return;
    }

    return paragraphs[activeChapter.chapter][activeChapter.paragraph].content;

  }

  useEffect(() => {

    axios.get(`/api/books/get/${slug}/simple`)
    .then((value) => value.data)
    .then((book) => {
      setBook(book)
      console.log(book)

      return book
    })
    .then((book) =>
    {
      updateActiveChapter({type: 'reset'});

      setParagraphs(prevState => []);
      axios.get(`/api/books/chapter/${book['id']}/paragraphs`)
      .then((value) => value.data)
      .then((data) =>
      {
        // console.log("data", data)
        let map = []

        for (let i = 0; i < data.length; i++)
        {
          let tmp = data[i];
          if(!(tmp.chapter_order in map))
          {
            map[tmp.chapter_order] = {}
          }
          map[tmp.chapter_order][tmp.paragraph_order]= tmp;
        }
        // console.log("MAP", map)
        setParagraphs(map);
      })

      axios.get(`/api/books/chapter/${book['id']}/paragraphs/count`)
      .then((value) => value.data)
      .then((limits) =>
      {
        // console.log("limits", limits);
        let limits_map = Object.assign({}, ...limits.map((x) => ({[x.chapter_order]: x.count})));
        let counts = Object.keys(limits_map).sort()
        let last_chapter = counts.pop()
        limits_map.length = last_chapter

        // console.log("limits_map", limits_map);
        updateActiveChapter({type: 'update', chapters: limits_map});
      });

    })
  }, [slug, setBook])

  const keypressHandler = ( e ) =>
  {
    if(e.key === "ArrowLeft")
    {
      updateActiveChapter({type: 'previous'})
    }
    if(e.key === "ArrowRight")
    {
      updateActiveChapter({type: 'next'})
    }
    console.log(e)
  }

  useEffect(() => {
    window.addEventListener("keydown", keypressHandler);

    return () => {
      window.removeEventListener("keydown", keypressHandler);
    };
  });

  if (book && activeChapter.chapters.length > 0) {
    if(book != null && paragraphs.length > activeChapter.chapter)
    {
      // var doc = new DOMParser().parseFromString(book.chapters[activeChapter.chapter].content, "text/html");
      // var text = doc.body.textContent.replaceAll("\n\n", "\n");
      // console.log("PP", activeChapter, paragraphs)
      return (
          <div className="App" id="#react-scroller">
            <BookNavbar
              chapter={paragraphs[activeChapter.chapter][activeChapter.paragraph]}
              book={book}
              // openToc={() => {
              //   setTocOpen(true);
              // }}
              visible={true}
            />

        <div className="flex-center position-ref full-height">
          <div className="container">
          <div className="content">
            <h3 dangerouslySetInnerHTML={{ __html: getActiveParagraph()}}></h3>
          </div>
          </div>
        </div>
        </div>
      );
    }
  }
  else
  {
    return null;
  }
  return null;
}

export default SimpleView;
