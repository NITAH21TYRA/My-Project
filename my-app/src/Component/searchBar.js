import React, { useState } from 'react';

const SearchBar = ({ products }) => {
  const [query, setQuery] = useState('');

  const handleSearch = () => {
    // Implement search functionality based on `query` and `products`
    console.log('Search query:', query);
  };

  return (
    <div className="search-bar">
      <input 
        type="text" 
        placeholder="Search..." 
        value={query} 
        onChange={(e) => setQuery(e.target.value)} 
      />
      <button onClick={handleSearch}>Search</button>
    </div>
  );
};

export default SearchBar;
