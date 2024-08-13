import { createSlice } from '@reduxjs/toolkit';
import { api } from '../../services/api';

const itinerariesSlice = createSlice({
  name: 'itineraries',
  initialState: {
    items: [],
    status: 'idle',
    error: null
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addMatcher(
        api.endpoints.getItineraries.matchFulfilled,
        (state, { payload }) => {
          state.items = payload;
          state.status = 'succeeded';
        }
      )
      .addMatcher(
        api.endpoints.getItineraries.matchPending,
        (state) => {
          state.status = 'loading';
        }
      )
      .addMatcher(
        api.endpoints.getItineraries.matchRejected,
        (state, action) => {
          state.status = 'failed';
          state.error = action.error.message;
        }
      );
  }
});

export default itinerariesSlice.reducer;