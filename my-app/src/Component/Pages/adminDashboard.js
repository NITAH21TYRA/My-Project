import React, { useState, useEffect } from "react";
import { useHistory } from "react-router-dom";
import "./adminDashboard.css"; // Import your custom CSS

const AdminDashboard = () => {
  const [orders, setOrders] = useState([]);
  const [products, setProducts] = useState([]);
  const [newProduct, setNewProduct] = useState({
    name: "",
    price: "",
    stock: "",
    image: "",
  });
  const [error, setError] = useState("");
  const history = useHistory();

  // Fetch both products and orders when the component mounts
  useEffect(() => {
    fetchProducts();
    fetchOrders();
  }, []);

  // Fetch all products from the API
  const fetchProducts = async () => {
    const token = localStorage.getItem("token"); // Use common token

    if (!token) {
      setError("No token found. Please log in.");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/api/v1/admin/products", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setProducts(data.products || []);
      } else {
        const errorData = await response.json();
        setError(errorData.message || "Failed to fetch products");
      }
    } catch (error) {
      console.error("Error fetching products:", error);
      setError("Error occurred while fetching products");
    }
  };

  // Fetch all orders from the API
  const fetchOrders = async () => {
    const token = localStorage.getItem("token"); // Use common token

    if (!token) {
      setError("No token found. Please log in.");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/api/v1/admin/orders", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setOrders(data.orders || []);
      } else {
        const errorData = await response.json();
        setError(errorData.message || "Failed to fetch orders");
      }
    } catch (error) {
      console.error("Error fetching orders:", error);
      setError("Error occurred while fetching orders");
    }
  };

  // Add a new product to the API
  const handleAddProduct = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token"); // Use common token

    if (!token) {
      setError("No token found. Please log in.");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/api/v1/admin/products", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(newProduct),
      });

      if (response.ok) {
        fetchProducts(); // Refresh the product list
        setNewProduct({ name: "", price: "", stock: "", image: "" });
        setError("");
      } else {
        const errorData = await response.json();
        setError(errorData.message || "Failed to add product");
      }
    } catch (error) {
      console.error("Error adding product:", error);
      setError("Error occurred while adding product");
    }
  };

  // Approve an order
  const handleApproveOrder = async (orderId) => {
    const token = localStorage.getItem("token"); // Use common token

    if (!token) {
      setError("No token found. Please log in.");
      return;
    }

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/v1/admin/orders/${orderId}/approve`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (response.ok) {
        fetchOrders(); // Refresh the order list after approval
      } else {
        const errorData = await response.json();
        setError(errorData.message || "Failed to approve order");
      }
    } catch (error) {
      console.error("Error approving order:", error);
      setError("Error occurred while approving order");
    }
  };

  // Handle form input changes for adding products
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewProduct((prevProduct) => ({
      ...prevProduct,
      [name]: value,
    }));
  };

  // Logout functionality
  const handleLogout = () => {
    localStorage.removeItem("token"); // Clear the common token
    history.push("/login");
  };

  return (
    <div className="admin-dashboard">
      <h2>Admin Dashboard</h2>
      <button onClick={handleLogout} className="logout-button">Logout</button>
      {error && <div className="error-message">{error}</div>}

      {/* Display Orders */}
      <section>
        <h3>Orders</h3>
        <table className="orders-table">
          <thead>
            <tr>
              <th>Order ID</th>
              <th>Customer</th>
              <th>Total</th>
              <th>Status</th>
              <th>Date</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {orders.length > 0 ? (
              orders.map((order) => (
                <tr key={order.id}>
                  <td>{order.id}</td>
                  <td>{order.customer_name}</td>
                  <td>{order.total}</td>
                  <td>{order.status}</td>
                  <td>{new Date(order.order_date).toLocaleString()}</td>
                  <td>
                    <button
                      onClick={() => handleApproveOrder(order.id)}
                      className="btn btn-approve"
                    >
                      Approve
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="6">No orders to display</td>
              </tr>
            )}
          </tbody>
        </table>
      </section>

      {/* Display Products */}
      <section>
        <h3>Products</h3>
        <table className="products-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Price</th>
              <th>Stock</th>
            </tr>
          </thead>
          <tbody>
            {products.length > 0 ? (
              products.map((product) => (
                <tr key={product.id}>
                  <td>{product.name}</td>
                  <td>{product.price}</td>
                  <td>{product.stock}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="3">No products to display</td>
              </tr>
            )}
          </tbody>
        </table>
      </section>

      {/* Add Product Form */}
      <section>
        <h3>Add Product</h3>
        <form onSubmit={handleAddProduct} className="add-product-form">
          <div className="form-group">
            <label>Name:</label>
            <input
              type="text"
              name="name"
              value={newProduct.name}
              onChange={handleInputChange}
              required
            />
          </div>
          <div className="form-group">
            <label>Price:</label>
            <input
              type="number"
              name="price"
              value={newProduct.price}
              onChange={handleInputChange}
              required
            />
          </div>
          <div className="form-group">
            <label>Stock:</label>
            <input
              type="number"
              name="stock"
              value={newProduct.stock}
              onChange={handleInputChange}
              required
            />
          </div>
          <div className="form-group">
            <label>Image URL:</label>
            <input
              type="text"
              name="image"
              value={newProduct.image}
              onChange={handleInputChange}
              required
            />
          </div>
          <button type="submit" className="btn btn-success">Add Product</button>
        </form>
      </section>
    </div>
  );
};

export default AdminDashboard;
