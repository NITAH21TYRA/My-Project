import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Switch, Route, Redirect } from 'react-router-dom';
import Navbar from './Component/Navbar';
import Products from './Component/Pages/Products';
import CreateAccount from './Component/Pages/CreateAccount';
import Order from './Component/Pages/Order';
import Cart from './Component/Pages/Cart';
import AdminDashboard from './Component/Pages/adminDashboard';
import AdminLogin from './Component/Pages/adminLogin';
import Login from './Component/Pages/Login';
import Footer from './Component/Footer';
import { CartProvider } from './Component/CartContext';
import { AuthProvider } from './Component/auth';
import './App.css';
import logo from './fierce__-removebg-preview.png';

function App() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    const fetchProducts = async () => {
      const adminToken = localStorage.getItem('adminToken');
      if (!adminToken) {
        console.error('Admin token not found');
        return;
      }

      try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/admin/products', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${adminToken}`,
          },
        });

        if (response.ok) {
          const data = await response.json();
          console.log('Products fetched:', data);
          setProducts(data.products || []);
        } else {
          console.error('Failed to fetch products:', response.statusText);
        }
      } catch (error) {
        console.error('Error fetching products:', error);
      }
    };

    fetchProducts();
  }, []);

  const isAdmin = localStorage.getItem('isAdmin') === 'true';

  const handleSearch = () => {
    // Implement search functionality if needed
  };

  return (
    <AuthProvider>
      <CartProvider>
        <div className="App">
          <header className="App-header">
            <div className="left-section">
              <img src={logo} className="App-logo" alt="logo" />
            </div>
            <div className="search-bar">
              <input className="active" type="text" placeholder="Search..." />
              <button onClick={handleSearch}>Search</button>
            </div>
          </header>

          <Router>
            <Navbar />
            <Switch>
              <Route path="/products" exact>
                <Products products={products} />
              </Route>
              <Route path="/cart" exact>
                <Cart />
              </Route>
              <Route path="/create-account" exact>
                <CreateAccount />
              </Route>
              <Route path="/order" exact>
                <Order />
              </Route>
              <Route path="/login" exact>
                <Login />
              </Route>
              <Route path="/admin/login" exact>
                <AdminLogin />
              </Route>
              {isAdmin ? (
                <Route path="/admin-dashboard" exact>
                  <AdminDashboard products={products} />
                </Route>
              ) : (
                <Redirect from="/admin-dashboard" to="/products" />
              )}
              <Redirect from="/" to={isAdmin ? "/admin-dashboard" : "/products"} />
              <Route path="*">
                <Redirect to={isAdmin ? "/admin-dashboard" : "/products"} />
              </Route>
            </Switch>
            <Footer />
          </Router>
        </div>
      </CartProvider>
    </AuthProvider>
  );
}

export default App;
