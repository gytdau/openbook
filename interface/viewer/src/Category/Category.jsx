import axios from 'axios';
import { useEffect, useState } from 'react';
import { Link, useParams, useHistory } from 'react-router-dom';


function Category() {
  let history = useHistory();
  const [selected_ids, setSelected] = useState([]);
  const [books, setBooks] = useState([]);
  const [categories, setCategories] = useState(null);
  const { category_ids } = useParams();

  useEffect(() => {
    if(category_ids == null)
      return;
    let ids = category_ids.split(',').map((id) => parseInt(id));
    setSelected((prev) => [...prev, ...ids])
  }, [category_ids]);

  useEffect(() => {
    if(category_ids == null)
    {
      setBooks([]);
      return;
    }
    axios.get(`/api/books/category/get/${category_ids}`).then((value) => {
      setBooks(value.data);
    });
  }, [category_ids, setBooks]);
  

  useEffect(() => {
    axios.get(`/api/books/categories/get`).then((value) => {
      setCategories(value.data);
    });
  }, [category_ids, setCategories]);

  if (books == null || categories == null) {
    return <p>Loading</p>;
  }

  const handleChange = (e) => {
    let toggle_id = parseInt(e.target.value);
    let checked = e.target.checked;
    if(checked)
    {
      setSelected((prev) => [...prev, toggle_id]);
    }
    else
    {
      setSelected((prev) => [...prev.filter((id) => id != toggle_id )]);
    }
  };

  function GetInputs(categories)
  {
    return categories.map(function(category) {
      return (
        <Checkbox label={category.name} value={category.id} checked={selected_ids.includes(category.id)} onChange={handleChange}/>
      )
    })
  }

  function filter()
  {
    let filtered_ids = selected_ids.filter((val) => Number.isInteger(val));
    let id_set = new Set(filtered_ids);
    history.push(`/category/${Array.from(id_set)}/`);
  }

  const Checkbox = ({ label, value, checked, onChange }) => {
    return (
      <div class="form-check col-6 col-md-3 col-lg-2 ">
        <label class="form-check-label">
          <input className='form-check-input' type="checkbox" value={value} checked={checked} onChange={onChange} />
          {label}
        </label>
      </div>
    );
  };

  return (
  <>
    <div className="container-fluid hero">
    <div className="container">
      <div className="row">
      <div className="col-md-12">
        <h1>Great ideas</h1>
        <h2>Read free books in the public domain.</h2>
      </div>
      </div>
    </div>
    </div>
    <div className="container my-3">
    <div className="row">
      <div className="col-md-12">
        <div className="row">
        {GetInputs(categories, category_ids)}
        </div>
        <div className="row">
          <button type="button" class="btn btn-primary" onClick={filter}>Filter</button>
        </div>
      </div>
      <div className="col-md-12">
        <div className="recommendations">
          <div className="top">
            <div className="recommendations-section-title">Book List</div>
            <div className="top-content">
            {books.map((book, index) => (
              <Link to={`/${book.slug}`} className="top-book">
              <div className="top-book__number">
                {index + 1}
                .
              </div>
              <div className="top-book__title">
                <h2>{book.author}</h2>
                <h1>{book.title}</h1>
              </div>
              </Link>
            ))}
            </div>
          </div>
        </div>
      </div>
    </div>
    </div>
  </>
  );
}
export default Category;
