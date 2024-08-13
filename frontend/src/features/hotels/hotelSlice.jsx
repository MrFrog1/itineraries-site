import { createSlice } from '@reduxjs/toolkit';
import { api } from '../../services/api';

const hotelsSlice = createSlice({
  name: 'hotels',
  initialState: {
    items: [],
    status: 'idle',
    error: null
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addMatcher(
        api.endpoints.getHotels.matchFulfilled,
        (state, { payload }) => {
          state.items = payload;
          state.status = 'succeeded';
        }
      )
      .addMatcher(
        api.endpoints.getHotels.matchPending,
        (state) => {
          state.status = 'loading';
        }
      )
      .addMatcher(
        api.endpoints.getHotels.matchRejected,
        (state, action) => {
          state.status = 'failed';
          state.error = action.error.message;
        }
      );
  }
});

export default hotelsSlice.reducer;