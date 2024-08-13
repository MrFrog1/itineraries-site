import { configureStore } from '@reduxjs/toolkit';
import { setupListeners } from '@reduxjs/toolkit/query';
import authReducer from '../features/auth/authSlice'; 
import { api } from '../services/api'; 
import regionReducer from '../features/regions/regionSlice'; // Add this import
import hotelsReducer from '../features/hotels/hotelSlice';
import itinerariesReducer from '../features/itineraries/itinerariesSlice';
import searchReducer from '../features/search/searchSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    [api.reducerPath]: api.reducer,
    region: regionReducer, // Add the region reducer
    hotels: hotelsReducer,
    itineraries: itinerariesReducer,
    search: searchReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(api.middleware),
});

setupListeners(store.dispatch);