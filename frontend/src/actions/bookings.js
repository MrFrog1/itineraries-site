import axios from "axios";

import {
  GET_BOOKINGS,
  GET_ERRORS,
  DELETE_BOOKING,
  UPDATE_BOOKING,
  ADD_BOOKING,
  GET_GROUPBOOKINGS,
  DELETE_GROUPBOOKING,
} from "./types";
 
 

export const getBookings = () => (dispatch) => {
  axios
    .get('http://localhost:8000/api/bookings/bookings/')
    .then((res) => {
      dispatch({
        type: GET_BOOKINGS, //When we dispatch this to the reducer, the switch(type) will determinw which type we are sending for.
        payload: res.data, //The payload needs to be the response data from the server.
      });
    })
    .catch((err) => {
      const errors = {
        msg: err.response.data,
        status: err.response.status,
      };
      dispatch({
        type: GET_ERRORS,
        payload: errors,
      });
    });
};

export const deleteBooking = (id) => (dispatch) => {
  axios
    .delete(`http://localhost:8000/api/bookings/bookings/${id}/`)
    .then((res) => {
      dispatch({
        type: DELETE_BOOKING, //When we dispatch this to the reducer, the switch(type) will determinw which type we are sending for.
        payload: id, //The payload needs to be the response data from the server.
      });
    })
    .catch((err) => {
      const errors = {
        msg: err.response.data,
        status: err.response.status,
      };
      dispatch({
        type: GET_ERRORS,
        payload: errors,
      });
    });
};

export const AddBooking = (data) => (dispatch) => {
  axios
    .post("http://localhost:8000/api/bookings/bookings/", data)
    .then((res) => {
      dispatch({
        type: ADD_BOOKING, //When we dispatch this to the reducer, the switch(type) will determinw which type we are sending for.
        payload: res.data, //The payload needs to be the response data from the server.
      });
    })
    .catch((err) => {
      const errors = {
        msg: err.response.data,
        status: err.response.status,
      };
      dispatch({
        type: GET_ERRORS,
        payload: errors,
      });
    });
};

export const updateBooking = (id) => (dispatch) => {
  axios
    .put(`http://localhost:8000/api/bookings/bookings/${id}/`)
    .then((res) => {
      dispatch({
        type: UPDATE_BOOKING, //When we dispatch this to the reducer, the switch(type) will determinw which type we are sending for.
        payload: res.data, //The payload needs to be the response data from the server.
      });
    })
    .catch((err) => {
      const errors = {
        msg: err.response.data,
        status: err.response.status,
      };
      dispatch({
        type: GET_ERRORS,
        payload: errors,
      });
    });
};

// https://stackoverflow.com/questions/45022857/chaining-redux-payload-with-axios look here for this below
// Do we keep group bookings and bookings intact before theyre in the front end?

// export const getFullBookings = () => dispatch => {
//     axios.all([
//         axios.get('http://localhost:8000/api/bookings/bookings/'),
//         axios.get('http://localhost:8000/api/bookings/group/')
//     ])
//     .then(axios.spread((bookings, group)=> {
//     });
//         dispatch({
//             type: GET_BOOKINGS,   //When we dispatch this to the reducer, the switch(type) will determinw which type we are sending for.
//             payload: res.data //The payload needs to be the response data from the server.
//         });
//     }).catch(err => console.log(err)); //in case there is an error. Can have an error reducer that sends errors down to our components.
// };
