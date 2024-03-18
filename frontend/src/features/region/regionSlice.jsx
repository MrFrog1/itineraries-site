import { createSlice } from '@reduxjs/toolkit';
import { api } from '../../services/api';

const initialState = {
  regions: [],
  status: 'idle',
  error: null,
};

const regionSlice = createSlice({
  name: 'region',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addMatcher(
        api.endpoints.getRegions.matchFulfilled,
        (state, { payload }) => {
          state.regions = payload;
          state.status = 'succeeded';
        }
      )
      .addMatcher(api.endpoints.getRegions.matchPending, (state) => {
        state.status = 'loading';
        state.error = null;
      })
      .addMatcher(api.endpoints.getRegions.matchRejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error;
      });
  },
});

export default regionSlice.reducer;