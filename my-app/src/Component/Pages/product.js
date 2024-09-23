// ProductItem.js
import React from 'react';
import { useCart } from '../CartContext';

const ProductItem = ({ product }) => {
  const { cartItems, setCartItems, totalPrice, setTotalPrice } = useCart();

  const addToCart = () => {
    const updatedCart = [...cartItems, product];
    setCartItems(updatedCart);

    const updatedTotalPrice = totalPrice + product.price;
    setTotalPrice(updatedTotalPrice);
  };

  return (
    <div className="product-item">
      <h2>{product.name}</h2>
      <p>Price: ${product.price}</p>
      <button onClick={addToCart}>Add to Cart</button>
    </div>
  );
};

export default ProductItem;
