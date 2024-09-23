import React, { useState, useEffect } from 'react';
import { useCart } from '../CartContext'; // Adjust the path as per your project structure

const Home = () => {
  const [products, setProducts] = useState([]); // Initialize as an empty array
  const { addToCart } = useCart(); // Destructure addToCart from useCart

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/products');
        const data = await response.json();
        setProducts(data.products || []); // Ensure products is always an array
      } catch (error) {
        console.error('Error fetching products:', error);
        setProducts([]); // Ensure products is an empty array in case of error
      }
    };

    fetchProducts();
  }, []);

  const handleAddToCart = (product) => {
    addToCart(product); // Add product to cart
    alert("Product added to cart!"); // Show plain alert message
  };

  return (
    <div className="home">
      <h2>
        <marquee style={{ backgroundColor: '#f0f0f0', padding: '10px' }}>
          Welcome to our store, dive into the world of our beautiful pieces
        </marquee>
      </h2>

      <div style={{ display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap' }}>
        {products.length > 0 ? (
          products.map((product) => (
            <div
              key={product.id}
              style={{
                border: '1px solid rgb(214, 154, 91)',
                width: '30%',
                marginRight: '0.5rem',
                marginBottom: '0.5rem',
                borderRadius: '0.5rem',
                marginTop: '0.5rem',
                textAlign: 'center',
                display: 'flex',
                flexDirection: 'column',
                padding: '1rem',
              }}
            >
              <img
                src={product.image}
                alt={product.name}
                style={{ width: 'calc(100% - 20px)', height: 'auto', borderRadius: '0.5rem', marginBottom: '1rem' }}
              />
              <div
                style={{
                  padding: '1rem',
                  border: '1px solid #ccc',
                  borderTop: 'none',
                  borderRadius: '0 0 0.5rem 0.5rem',
                  backgroundColor: 'rgb(205, 152, 102)',
                  color: 'white',
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'space-between',
                }}
              >
                <h2>{product.name}</h2>
                <p>Price: {Math.round(product.price)}</p>
                <p>Stock: {product.stock}</p>
                <button
                  style={{
                    width: '100%',
                    padding: '0.75rem',
                    backgroundColor: '#ca8d5b',
                    color: 'white',
                    border: 'none',
                    borderRadius: '0.25rem',
                    cursor: 'pointer',
                  }}
                  onClick={() => handleAddToCart(product)}
                >
                  Add to Cart
                </button>
              </div>
            </div>
          ))
        ) : (
          <p>No products available.</p>
        )}
      </div>
    </div>
  );
};

export default Home;
