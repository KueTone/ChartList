import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './components/home';
import TopAffordablePlaces from './components/TopAffordablePlaces';
import PropertyTypeComparison from './components/PropertyTypeComparison';
// import PriceDistributionComparison from './components/PriceDistributionComparison';
// import CheapestAreas from './components/CheapestAreas';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/top-affordable-places" element={<TopAffordablePlaces />} />
        <Route path="/property-type-comparison" element={<PropertyTypeComparison />} />
        </Routes>
    </Router>
  );
}

export default App;
