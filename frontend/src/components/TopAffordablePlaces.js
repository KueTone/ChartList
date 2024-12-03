import React, { useEffect, useState } from 'react';
import { getTopAffordablePlaces } from '../services/api';

const TopAffordablePlaces = () => {
  const [places, setPlaces] = useState([]);

  useEffect(() => {
    getTopAffordablePlaces().then((response) => {
      setPlaces(response.data.top_affordable_places);
    }).catch((error) => {
      console.error('Error fetching data:', error);
    });
  }, []);

  return (
    <div>
      <h2>Top 10 Affordable Places</h2>
      <table>
        <thead>
          <tr>
            <th>Place Name</th>
            <th>Average Price</th>
            <th>Total Listings</th>
          </tr>
        </thead>
        <tbody>
          {places.map((place, index) => (
            <tr key={index}>
              <td>{place.place_name}</td>
              <td>{place.avg_price}</td>
              <td>{place.total_listings}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TopAffordablePlaces;
