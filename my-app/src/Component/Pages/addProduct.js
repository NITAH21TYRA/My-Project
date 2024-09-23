import React, { useState } from 'react';
import './addProduct.css';

const AddProduct = () => {
  const [name, setName] = useState('');
  const [price, setPrice] = useState('');
  const [stock, setStock] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://127.0.0.1:5000/api/v1/product/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ name, price, stock }),
      });
      const data = await response.json();

      if (response.ok) {
        setMessage('Product added successfully');
        setName('');
        setPrice('');
        setStock('');
      } else {
        setMessage(data.message || 'Failed to add product');
      }
    } catch (error) {
      console.error('Add product error:', error);
      setMessage('An error occurred. Please try again.');
    }
  };

  return (
    <div className="add-product-container">
      <h3>Add Product</h3>
      {message && <p>{message}</p>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Name:</label>
          <input 
            type="text" 
            value={name} 
            onChange={(e) => setName(e.target.value)} 
            required 
          />
        </div>
        <div className="form-group">
          <label>Price:</label>
          <input 
            type="text" 
            value={price} 
            onChange={(e) => setPrice(e.target.value)} 
            required 
          />
        </div>
        <div className="form-group">
          <label>Stock:</label>
          <input 
            type="text" 
            value={stock} 
            onChange={(e) => setStock(e.target.value)} 
            required 
          />
        </div>
        <button type="submit" className="btn">Add Product</button>
      </form>
    </div>
  );
};

export default AddProduct;
