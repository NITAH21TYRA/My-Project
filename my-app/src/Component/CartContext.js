// CartContext.js
import React, { createContext, useContext, useState } from 'react';

const CartContext = createContext();

export const useCart = () => useContext(CartContext);

export const CartProvider = ({ children }) => {
  const [cartItems, setCartItems] = useState([]);
  const [totalPrice, setTotalPrice] = useState(0);

  const addToCart = (product) => {
    const updatedCart = [...cartItems, product];
    setCartItems(updatedCart);

    const updatedTotalPrice = totalPrice + product.price;
    setTotalPrice(updatedTotalPrice);
  };

  const removeCartItem = (productId) => {
    const updatedCart = cartItems.filter(item => item.id !== productId);
    setCartItems(updatedCart);

    const updatedTotalPrice = updatedCart.reduce((total, item) => total + item.price, 0);
    setTotalPrice(updatedTotalPrice);
  };

  const clearCart = () => {
    setCartItems([]);
    setTotalPrice(0);
  };

  return (
    <CartContext.Provider value={{ cartItems, totalPrice, addToCart, removeCartItem, clearCart }}>
      {children}
    </CartContext.Provider>
  );
};
