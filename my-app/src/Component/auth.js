import React, { createContext, useState, useEffect, useCallback } from 'react';

// Create the context
const AuthContext = createContext();

// Create a provider component
const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  // Function to log in a user
  const login = async (email, password) => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/v1/user/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      const data = await response.json();
      if (response.ok) {
        setUser(data.user);
        localStorage.setItem('token', data.token); // Save user token
      } else {
        throw new Error(data.message || 'Failed to log in');
      }
    } catch (error) {
      console.error('Login error:', error);
    }
  };

  // Function to log out a user
  const logout = () => {
    setUser(null);
    localStorage.removeItem('token'); // Remove the user token
    localStorage.removeItem('adminToken'); // Remove the admin token
    localStorage.removeItem('isAdmin'); // Remove admin status
  };

  // Function to check if a user is authenticated
  const isAuthenticated = () => !!user;

  // Function to fetch user data based on stored token
  const fetchUserData = useCallback(async () => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/user/me', {
          method: 'GET',
          headers: { 'Authorization': `Bearer ${token}` },
        });
        const data = await response.json();
        if (response.ok) {
          setUser(data.user);
        } else {
          logout(); // Log out if the token is invalid
        }
      } catch (error) {
        console.error('Fetch user data error:', error);
        logout();
      }
    }
  }, []);

  useEffect(() => {
    fetchUserData();
  }, [fetchUserData]);

  return (
    <AuthContext.Provider value={{ user, login, logout, isAuthenticated }}>
      {children}
    </AuthContext.Provider>
  );
};

export { AuthContext, AuthProvider };
