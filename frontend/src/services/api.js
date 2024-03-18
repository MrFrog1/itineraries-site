import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import { setUser, logoutUser } from '../features/auth/authSlice'; // Adjust the path as necessary

// Function to get CSRF token from cookies
function getCsrfToken() {
    const csrfToken = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
    return csrfToken ? csrfToken.split('=')[1] : null;
}

// Base query with automatic token refresh
const baseQueryWithReauth = async (args, api, extraOptions) => {
    let result = await fetchBaseQuery({ 
        baseUrl: 'http://localhost:8000/',
        prepareHeaders: (headers, { getState }) => {
            const csrfToken = getCsrfToken();
            if (csrfToken) {
                headers.set('X-CSRFToken', csrfToken);
            }

            const token = getState().auth.token?.access; // Ensure you are getting the 'access' token
            if (token) {
                headers.set('Authorization', `Bearer ${token}`);
            }
            return headers;
        },
        credentials: 'include', // Important for sending and receiving HTTP-only cookies
    })(args, api, extraOptions);

    // Automatically refresh token if response is 401 (Unauthorized)
    if (result.error && result.error.status === 401) {
        // Attempt to refresh token using the original fetchBaseQuery
        const refreshResult = await fetchBaseQuery({
            baseUrl: 'http://localhost:8000/',
            credentials: 'include', // Important for sending and receiving HTTP-only cookies
            prepareHeaders: (headers) => {
                const csrfToken = getCsrfToken();
                if (csrfToken) {
                    headers.set('X-CSRFToken', csrfToken);
                }
                return headers;
            },
        })({ url: 'token/refresh/', method: 'POST' }, api, extraOptions);

        if (refreshResult.data) {
            // Update state with new tokens
            api.dispatch(setUser({ token: refreshResult.data.access })); // Update only access token as refresh token is in HTTP-only cookie
            // Retry the original query with new access token
            result = await fetchBaseQuery({ 
                baseUrl: 'http://localhost:8000/',
                prepareHeaders: (headers) => {
                    if (refreshResult.data.access) {
                        headers.set('Authorization', `Bearer ${refreshResult.data.access}`);
                    }
                    return headers;
                },
                credentials: 'include',
            })(args, api, extraOptions);
        } else {
            // Logout user if token refresh fails
            api.dispatch(logoutUser());
        }
    }

    return result;
};


export const api = createApi({
    reducerPath: 'api',
    baseQuery: baseQueryWithReauth,
    endpoints: (builder) => ({
        loginUser: builder.mutation({
            query: (credentials) => ({
                url: 'token/',
                method: 'POST',
                body: credentials,
            }),
        }),
        getRegions: builder.query({
        query: () => 'regions',
        }),
        registerUser: builder.mutation({
            query: (user) => ({
                url: 'register/', // Make sure this matches your Django URL
                method: 'POST',
                body: user,
            }),
            // Optional: Adjust the response structure if necessary
            transformResponse: (response, meta, arg) => {
                // You can transform the response here if needed
                return response;
            },
        }),
        // Add other endpoints as necessary
    }),
});

export const { useLoginUserMutation, useRegisterUserMutation, useGetRegionsQuery  } = api;