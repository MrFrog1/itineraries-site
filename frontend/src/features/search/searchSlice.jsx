import { api } from '../../services/api'; // Make sure this path is correct
import { createSlice, createSelector } from '@reduxjs/toolkit';

const searchSlice = createSlice({
  name: 'search',
  initialState: {
    searchParams: {
      activeTab: 'itineraries',
      location: '',
      type: '',
      minPrice: '',
      maxPrice: '',
      hoursFrom: '',
      hoursMode: 'driving',
      selectedButtons: [],
      month: '',
      bestFor: '',
    },
  },
  reducers: {
    setSearchParams: (state, action) => {
      state.searchParams = { ...state.searchParams, ...action.payload };
    },
  },
});

export const { setSearchParams } = searchSlice.actions;

export default searchSlice.reducer;

// Selector for filtered results
export const selectFilteredResults = (state) => {
  const { searchParams } = state.search;
  const { hotels, itineraries, regions } = state.api.queries;

  const getQueryData = (queryName) => {
    const queryData = Object.values(state.api.queries).find(query => query.endpointName === queryName);
    return queryData ? queryData.data : [];
  };

  const hotelsData = getQueryData('getHotels') || [];
  const itinerariesData = getQueryData('getItineraries') || [];
  const regionsData = getQueryData('getRegions') || [];

  const filterItem = (item) => {
    const matchesLocation = !searchParams.location || searchParams.location.split(',').some(loc => 
      item.region.name.toLowerCase().includes(loc.toLowerCase())
    );
    const matchesType = !searchParams.type || searchParams.type.split(',').some(type => 
      item.type.toLowerCase() === type.toLowerCase()
    );
    const price = searchParams.activeTab === 'hotels' ? item.min_price_in_INR : item.cost_for_1_pax;
    const matchesPrice = (!searchParams.minPrice || price >= parseInt(searchParams.minPrice)) &&
                         (!searchParams.maxPrice || price <= parseInt(searchParams.maxPrice));
    return matchesLocation && matchesType && matchesPrice;
  };

  const filterRegion = (region) => {
    const matchesMonth = !searchParams.month || region.best_months.includes(searchParams.month);
    const matchesBestFor = !searchParams.bestFor || region.best_for.includes(searchParams.bestFor);
    return matchesMonth && matchesBestFor;
  };

  const filteredHotels = searchParams.activeTab === 'hotels' ? hotelsData.filter(filterItem) : [];
  const filteredItineraries = searchParams.activeTab === 'itineraries' ? itinerariesData.filter(filterItem) : [];
  const filteredRegions = regionsData.filter(filterRegion);

  return { hotels: filteredHotels, itineraries: filteredItineraries, regions: filteredRegions };
};

// Add this to ensure the api reducer is included in the store
export const { reducer: apiReducer } = api;