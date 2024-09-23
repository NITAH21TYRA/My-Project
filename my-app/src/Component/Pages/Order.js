import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import './Order.css';

const Order = () => {
  const [orders, setOrders] = useState([]);
  const history = useHistory();

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          alert('Please log in to view your orders');
          history.push('/login');
          return;
        }

        const response = await fetch('http://127.0.0.1:5000/api/v1/orders', {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
        const data = await response.json();
        setOrders(data.orders);
      } catch (error) {
        console.error('Error fetching orders:', error);
      }
    };

    fetchOrders();
  }, [history]);

  return (
    <div className="orders">
      <h1>Your Orders</h1>
      <div className="orders-list">
        {orders.length ? (
          orders.map((order) => (
            <div key={order.id} className="order-item">
              <div>Order ID: {order.id}</div>
              <div>Total Price: ${order.total_price}</div>
              <div>Status: {order.status}</div>
              <div>Created At: {new Date(order.created_at).toLocaleString()}</div>
              <div>Updated At: {new Date(order.updated_at).toLocaleString()}</div>
              <div>
                <strong>Items:</strong>
                <ul>
                  <li>Product ID: {order.product_id} - Quantity: {order.quantity}</li>
                </ul>
              </div>
            </div>
          ))
        ) : (
          <div>No orders found</div>
        )}
      </div>
    </div>
  );
};

export default Order;
