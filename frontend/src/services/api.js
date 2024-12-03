import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
});

export const getBlockValues = () => api.get('/block-values');
export const getTopAffordablePlaces = () => api.get('/top-affordable-places');
export const getPropertyTypeComparison = () => api.get('/property-type-comparison');
export const getPriceDistributionComparison = () => api.get('/price-distribution-comparison');
export const getCheapestAreas = () => api.get('/cheapest-areas');
