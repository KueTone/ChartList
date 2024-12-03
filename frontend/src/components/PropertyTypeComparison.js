import React, { useEffect, useState } from 'react';
import { getPropertyTypeComparison } from '../services/api';

const PropertyTypeComparison = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch property type comparison data
    getPropertyTypeComparison()
      .then((response) => {
        setData(response.data.property_type_comparison);
        setLoading(false);
      })
      .catch((err) => {
        setError('Error fetching property type comparison data');
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  return (
    <div>
      <h2>Property Type Comparison</h2>
      <table>
        <thead>
          <tr>
            <th>Property Type</th>
            <th>Average Price</th>
            <th>Number of Listings</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr key={index}>
              <td>{item.property_type}</td>
              <td>{item.avg_price.toFixed(2)}</td>
              <td>{item.number_of_listings}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default PropertyTypeComparison;