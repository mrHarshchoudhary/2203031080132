import React, { useEffect, useState } from "react";
import axios from "axios";

const BookManager = () => {
  const [books, setBooks] = useState([]);
  const [form, setForm] = useState({ title: "", author: "", price: "" });

  const loadBooks = async () => {
    try {
      const res = await axios.get("http://localhost:5000/api/books");
       setBooks(res.data);
    } catch (err) {
      console.error("Error loading books:", err.message);
    }
  };

  useEffect(() => {
    loadBooks();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://localhost:5000/api/books", form);
      setForm({ title: "", author: "", price: "" });
      loadBooks();
    } catch (err) {
      alert("Error adding book");
    }
  };

  const deleteBook = async (id) => {
    try {
      await axios.delete(`http://localhost:5000/api/books/${id}`);
      loadBooks();
    } catch (err) {
      alert("Error deleting book");
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h2>📚 Book Manager</h2>

      <form onSubmit={handleSubmit} style={{ marginBottom: "20px" }}>
        <input
          placeholder="Title"
          value={form.title}
          onChange={(e) => setForm({ ...form, title: e.target.value })}
          required
        />
        <input
          placeholder="Author"
          value={form.author}
          onChange={(e) => setForm({ ...form, author: e.target.value })}
          required
        />
        <input
          placeholder="Price"
          type="number"
          value={form.price}
          onChange={(e) => setForm({ ...form, price: e.target.value })}
          required
        />
        <button type="submit">Add Book</button>
      </form>

      {books.length === 0 ? (
        <p>No books found.</p>
      ) : (
        <ul>
          {books.map((book) => (
            <li key={book.id}>
              <strong>{book.title}</strong> by {book.author} — ₹{book.price}{" "}
              <button onClick={() => deleteBook(book.id)}>❌</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default BookManager;
