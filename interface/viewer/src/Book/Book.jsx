import axios from 'axios';
import { useEffect, useState } from 'react';
import { Redirect, useParams } from 'react-router-dom';
import BookView from './BookView';

function Book() {
  const { slug, chapterSlug } = useParams();

  const [book, setBook] = useState(null);
  const [categories, setCategories] = useState(null);

  useEffect(() => {
    axios.get(`/api/books/get/${slug}`).then((value) => {
      setBook(value.data);
    });
  }, [slug, setBook]);

  useEffect(() => {
    axios.get(`/api/books/get/${slug}/categories`).then((value) => {
      setCategories(value.data);
    });
  }, [slug, setCategories]);

  if (book == null || categories == null) {
    return <p>Loading</p>;
  }
  if (chapterSlug == null) {
    return <Redirect to={`${slug}/${book.chapters[0].slug}`} />;
  }
  return <BookView book={book} chapterSlug={chapterSlug} categories={categories} />;
}

export default Book;
