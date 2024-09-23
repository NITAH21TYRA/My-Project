import React, { useContext } from 'react';
import { useCart } from '../CartContext';
import { AuthContext } from '../auth';
import './Cart.css'; // Import your CSS file

const Cart = () => {
  const { cartItems, totalPrice, removeCartItem } = useCart();
  const { user } = useContext(AuthContext);

  const createOrder = async () => {
    if (!user) {
      console.log('User not logged in. Redirecting to login page...');
      return;
    }

    const clientDetails = {
      name: user.name,
      address: user.address
    };

    const orderData = {
      client: clientDetails,
      cartItems: cartItems,
      totalPrice: totalPrice
    };

    try {
      const response = await fetch('http://127.0.0.1:5000/api/v1/orders', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(orderData)
      });

      if (response.ok) {
        console.log('Order created successfully.');

        // Optional: Send an email notification after the order is created
        const emailData = {
          client: clientDetails,
          orderItems: cartItems,
          totalPrice: totalPrice
        };

        try {
          const emailResponse = await fetch('http://127.0.0.1:5000/api/v1/notification/send-email', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(emailData)
          });

          if (emailResponse.ok) {
            console.log('Email notification sent successfully.');
          } else {
            console.error('Failed to send email notification:', emailResponse.statusText);
          }
        } catch (error) {
          console.error('Error sending email notification:', error);
        }

      } else {
        console.error('Failed to create order:', response.statusText);
      }
    } catch (error) {
      console.error('Error creating order:', error);
    }
  };

  return (
    <div className="cart">
      <h2>Cart</h2>
      <ul className="cart-list">
        {cartItems.map((item, index) => (
          <li key={index} className="cart-item">
            <span>{item.name}</span>
            <span>{item.price}</span>
            <button onClick={() => removeCartItem(item.id)} className="remove-button">Remove</button>
          </li>
        ))}
      </ul>
      <p>Total Price: {totalPrice}</p>
      <button onClick={createOrder}>Order</button>
    </div>
  );
};

export default Cart;
