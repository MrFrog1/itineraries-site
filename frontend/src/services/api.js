import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import { setUser, logoutUser } from '../features/auth/authSlice';

// function getCsrfToken() {
//     const csrfToken = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
//     return csrfToken ? csrfToken.split('=')[1] : null;
// }

const baseQuery = fetchBaseQuery({
    baseUrl: 'http://localhost:8000/',
    prepareHeaders: (headers, { getState }) => {
        const token = getState().auth.token;
        if (token) {
            headers.set('authorization', `Bearer ${token}`);
        }
        return headers;
    },
    credentials: 'include',
});

const baseQueryWithReauth = async (args, api, extraOptions) => {
    let result = await baseQuery(args, api, extraOptions);
    if (result.error && result.error.status === 401) {
        // Try to get a new token
        const refreshResult = await baseQuery({
            url: 'o/token/',
            method: 'POST',
            body: new URLSearchParams({
                'grant_type': 'refresh_token',
                'client_id': 'Azi3XQLAUoEXJpYAO9A17FtXATlAK11bIeMlUOmM',
                'client_secret': 'FH4f7Vpk8m5WT8kSls6WhHlYyowHwmkdtDAEK7cSQp4OIx1HTBr9AfonLwQgK6faixmTRHEPflfQNRr0pcbv9qynymS3Pq9bxmJllf5siXJP4BokbemWnHnqUovDSnNF',
            }),
        }, api, extraOptions);
        if (refreshResult.data) {
            // Store the new token
            api.dispatch(setUser(refreshResult.data));
            // Retry the original query with new access token
            result = await baseQuery(args, api, extraOptions);
        } else {
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
                url: 'o/token/',
                method: 'POST',
                body: new URLSearchParams({
                    'grant_type': 'password',
                    'username': credentials.username,
                    'password': credentials.password,
                    'client_id': 'Azi3XQLAUoEXJpYAO9A17FtXATlAK11bIeMlUOmM',
                    'client_secret': 'FH4f7Vpk8m5WT8kSls6WhHlYyowHwmkdtDAEK7cSQp4OIx1HTBr9AfonLwQgK6faixmTRHEPflfQNRr0pcbv9qynymS3Pq9bxmJllf5siXJP4BokbemWnHnqUovDSnNF',
        }),
      }),
    }),
    registerUser: builder.mutation({
      query: (user) => ({
        url: 'register/',
        method: 'POST',
        body: user,
      }),
    }),
    addHotel: builder.mutation({
      query: (hotelData) => ({
        url: 'api/hotels',
        method: 'POST',
        body: hotelData,
      }),
    }),
    addAgentHotel: builder.mutation({
      query: (hotelData) => ({
        url: 'api/hotels/agent_hotels',
        method: 'POST',
        body: hotelData,
      }),
    }),
    addCustomizedHotel: builder.mutation({
      query: (hotelData) => ({
        url: 'api/hotels/customized_hotels',
        method: 'POST',
        body: hotelData,
      }),
    }),
    searchAgents: builder.query({
      query: (term) => `api/agents/search?q=${term}`,
      transformResponse: (response) => {
        console.log('API Response:', response);
        return response.data || [];
      },
    }),
    addComponent: builder.mutation({
      query: (componentData) => ({
        url: 'api/components/components',
        method: 'POST',
        body: componentData,
      }),
    }),
    addContact: builder.mutation({
      query: (data) => ({
        url: 'api/contacts/contacts',
        method: 'POST',
        body: data,
      }),
    }),
    addContactCategory: builder.mutation({
      query: (data) => ({
        url: 'api/contacts/contact_categories',
        method: 'POST',
        body: data,
      }),
    }),
    addContactBusiness: builder.mutation({
      query: (data) => ({
        url: 'api/contacts/contact_businesses',
        method: 'POST',
        body: data,
      }),
    }),
    addComponentType: builder.mutation({
      query: (data) => ({
        url: 'api/components/component_types',
        method: 'POST',
        body: data,
      }),
    }),
    getAllComponentTypes: builder.query({
      query: () => 'api/components/component_types',
    }),
    getComponentTypes: builder.query({
      query: (agentId) => `api/components/component_types?agent_id=${agentId}`,
    }),
    addPhoto: builder.mutation({
      query: (photoData) => ({
        url: 'api/media/photos',
        method: 'POST',
        body: photoData,
      }),
    }),
    addAgentItinerary: builder.mutation({
      query: (itineraryData) => ({
        url: 'api/itineraries/',
        method: 'POST',
        body: itineraryData,
      }),
    }),
    addAgent: builder.mutation({
      query: (agentData) => ({
        url: 'api/agents/create',
        method: 'POST',
        body: agentData,
      }),
    }),
    addPotentialAgent: builder.mutation({
      query: (potentialAgentData) => ({
        url: 'api/potential-agents/create',
        method: 'POST',
        body: potentialAgentData,
      }),
    }),
    getAllPotentialAgents: builder.query({
      query: () => 'api/potential-agents',
    }),
    getRegions: builder.query({
      query: () => 'api/regions',
      transformResponse: (response) => {
        console.log('Regions API Response:', response);
        return response || [];
      },
    }),
    getDetailedRegions: builder.query({ 
      query: () => 'api/regions/detailed',
    }),
    getContacts: builder.query({
      query: () => 'api/contacts/contacts',
    }),
    getComponents: builder.query({
      query: (agentId) => `api/components/components?agent_id=${agentId}`,
    }),
    getItineraryGroups: builder.query({
      query: (agentId) => `api/itineraries/itinerary_groups?agent_id=${agentId}`,
    }),
    getItineraryDays: builder.query({
      query: (agentId) => `api/itineraries/itinerary_days?agent_id=${agentId}`,
    }),
    getAgentItineraries: builder.query({
      query: (agentId) => `api/itineraries/${agentId ? `?agent=${agentId}` : ''}`,
    }),
    getContactCategories: builder.query({
      query: () => 'api/contacts/contact_categories',
    }),
    getContactBusinesses: builder.query({
      query: () => 'api/contacts/contact_businesses',
    }),
    chat: builder.mutation({
      query: (message) => ({
        url: 'api/search/chat/',
        method: 'POST',
        body: { message },
      }),
    }),
    getHotels: builder.query({
      query: () => 'api/hotels',
    }),
    getItineraries: builder.query({
      query: () => 'api/itineraries',
    }),
    getHotelDetails: builder.query({
      query: (id) => `api/hotels/${id}`,
    }),
    getItineraryDetails: builder.query({
      query: (id) => `api/itineraries/${id}`,
    }),
    searchItems: builder.query({
      query: (params) => ({
        url: 'api/search',
        params: {
          type: params.activeTab,
          location: params.location,
          item_type: params.type,
          min_price: params.minPrice,
          max_price: params.maxPrice,
          hours_from: params.hoursFrom,
          travel_mode: params.hoursMode,
          tags: params.selectedButtons.join(','),
          month: params.month,
          best_for: params.bestFor,
        },
      }),
    }),
    getHotelPhotos: builder.query({
      query: (hotelId) => `api/photos?hotel_id=${hotelId}`,
    }),
    getItineraryPhotos: builder.query({
      query: (itineraryId) => `api/photos?itinerary_id=${itineraryId}`,
    }),
    getAgent: builder.query({
      query: (agentId) => `api/agents/${agentId}`,
    }),
    getAllAgents: builder.query({
      query: () => 'api/agents',
      transformResponse: (response) => {
        console.log('All Agents API Response:', response);
        return response || [];
      },
    }),
  }),
});

    // getDetailedRegions: builder.mutation({
    //   query: (ids) => ({
    //     url: 'api/regions/detailed',
    //     method: 'POST',
    //     body: { ids },
    //   }),
    // }),
    

export const {
  useAddHotelMutation,
  useAddAgentHotelMutation,
  useAddCustomizedHotelMutation,
  useSearchAgentsQuery,
  useAddComponentMutation,
  useAddComponentTypeMutation,
  useAddPhotoMutation,
  useAddAgentItineraryMutation,
  useAddAgentMutation,  
  useAddContactMutation,  
  useAddContactCategoryMutation,  
  useAddContactBusinessMutation,  
  useAddPotentialAgentMutation,
  useLoginUserMutation,
  useRegisterUserMutation,
  useGetComponentsQuery, 
  useGetRegionsQuery,
  useGetDetailedRegionsQuery,
  useGetContactsQuery,
  useGetContactCategoriesQuery,
  useGetContactBusinessesQuery,
  useGetHotelsQuery,
  useGetItinerariesQuery,
  useGetAgentItinerariesQuery,
  useGetItineraryGroupsQuery,
  useGetItineraryDaysQuery,
  useGetAllComponentTypesQuery,
  useGetComponentTypesQuery,
  useGetHotelDetailsQuery,
  useGetItineraryDetailsQuery,
  useSearchItemsQuery,
  useGetHotelPhotosQuery,
  useGetItineraryPhotosQuery,
  useGetAgentQuery,
  useGetAllAgentsQuery,
  useGetAllPotentialAgentsQuery,
  useChatMutation,
  
} = api;

