import { createSlice } from '@reduxjs/toolkit';
import { api } from '../../services/api'; // Ensure this path is correct

const initialState = {
    user: null, // Start with no user
    token: null, // Now this will only store the access token if necessary
    status: 'idle', // 'idle' | 'loading' | 'succeeded' | 'failed'
    error: null,
};

const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        logoutUser(state) {
            // Clear user and token information from Redux state
            state.user = null;
            state.token = null;
            state.status = 'idle';
            state.error = null;

            // Clear user info from localStorage if you were storing it there
            localStorage.removeItem('user');
        },
        setUser(state, action) {
            const { user, token } = action.payload;
            if (user) {
                // Update Redux state with the new user information
                state.user = user;

                // Optionally, update user info in localStorage
                // localStorage.setItem('user', JSON.stringify(user));
            }
            if (token) {
                // Only store access token in Redux state if necessary
                state.token = token.access;
            }
            state.status = 'succeeded'; // Update status to reflect successful login
        }
    },
    extraReducers: (builder) => {
        builder
            .addMatcher(
                api.endpoints.loginUser.matchFulfilled,
                (state, { payload }) => {
                    if (payload.user) {
                        // Set user based on login response
                        state.user = payload.user;
                        // Only update the token in state if you need to store the access token
                        state.token = payload.token.access;
                        state.status = 'succeeded';
                    }
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
