import React from 'react';
import { Routes, Route } from 'react-router-dom';
import HomePage from './components/HomePage';
import ProductDetail from './components/ProductDetail';
import './App.css';

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/produto/:productId" element={<ProductDetail />} />
    </Routes>
  );
}

export default App;
