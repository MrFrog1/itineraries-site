import { createSlice } from '@reduxjs/toolkit';
import { api } from '../../services/api';

const initialState = {
    user: null,
    token: null,
    status: 'idle',
    error: null,
};

const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        logoutUser(state) {
            state.user = null;
            state.token = null;
            state.status = 'idle';
            state.error = null;
            localStorage.removeItem('user');
        },
        setUser: (state, action) => {
        const { access_token, refresh_token, ...userData } = action.payload;
        state.user = userData;
        state.token = access_token;
        },
    },
    extraReducers: (builder) => {
        builder
            .addMatcher(
                api.endpoints.loginUser.matchFulfilled,
                (state, { payload }) => {
                    const { access_token, ...user } = payload;
                    state.user = user;
                    state.token = access_token;
                    state.status = 'succeeded';
                }
            )
            .addMatcher(api.endpoints.loginUser.matchPending, (state) => {
                state.status = 'loading';
                state.error = null;
            })
            .addMatcher(api.endpoints.loginUser.matchRejected, (state, action) => {
                state.status = 'failed';
                state.error = action.error;
                state.user = null;
                state.token = null;
            });
    },
});

export const { logoutUser, setUser } = authSlice.actions;
export default authSlice.reducer;