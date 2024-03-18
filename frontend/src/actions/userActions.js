import axios from "axios";
 
import {
  USER_SELECT,
  CHANGE_HOTEL_VIEW,
  LOG_OUT,
  AUTH_ERROR,
  USER_LOADING,
  GET_ERRORS,
  USER_LOGIN,
} from "./types";
// import { returnErrors } from './messages';

export const logUserOut = () => (dispatch) => {
  localStorage.removeItem("token");
  dispatch({
    type: LOG_OUT,
  });
};

export const userError = () => (dispatch) => {
  // This error handles an error with authentication
  localStorage.removeItem("token");
  dispatch({
    type: AUTH_ERROR,
  });
};

export const fetchUser = (userInfo) => (dispatch) => {
  // This action is for when a client logs in. It returns the token and sets it to local storage, along with the user information

  const config = {
    headers: {
      "Content-Type": "application/json",
      accept: "application/json",
    },
  };

  axios
    .post("http://localhost:8000/token-auth/", userInfo, config)
    .then((res) => {
      localStorage.setItem("token", res.data["token"]);
      axios.defaults.headers.common[
        "Authorization"
      ] = `JWT ${res.data["token"]}`;
      axios.defaults.headers.common["Content-Type"] = "application/json";
      axios.defaults.headers.common["accept"] = "application/json";

      dispatch({
        type: USER_LOGIN, //When we dispatch this to the reducer, the switch(type) will determinw which type we are sending for.
        payload: res.data["user"], //The payload needs to be the response data from the server.
        payload2: res.data["user"]["default_hotel"],
      });
    })
    .catch((err) => {
      console.log(err)
      // const errors = {
      //   msg: err.response,
      //   status: err.response.status,
      // };
      // dispatch({
      //   type: AUTH_ERROR,
      // });
      // dispatch({
      //   type: GET_ERRORS,
      //   payload: errors,
      // });
    });
};

export const signUserUp = (userInfo) => (dispatch) => {
  // This also returns the user object, but when the sign up  information is posted to the token handler.
  axios
    .post("http://localhost:8000/auth/users/", userInfo, {
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    })
    .then((res) => {
      localStorage.setItem("token", res.token);
      axios.defaults.headers.common[
        "Authorization"
      ] = `JWT ${res.data["token"]}`;
      axios.defaults.headers.common["Content-Type"] = "application/json";
      axios.defaults.headers.common["accept"] = "application/json";

      dispatch({
        type: USER_LOGIN, //When we dispatch this to the reducer, the switch(type) will determinw which type we are sending for.
        payload: res.user, //The payload needs to be the response data from the server.
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

export const autoLogin = () => (dispatch) => {
  // This function just double checks user details periodically and returns back to state.

  // First, we dispatch the action that the user is loading

  dispatch({ type: USER_LOADING });

  const token = localStorage.getItem("token");

  // We then add the token to the header if it exists.

  if (token) {
    axios.defaults.headers.common["Authorization"] = `JWT ${token}`;
  }

  axios
    .get("http://localhost:8000/auth/current_user/")
    .then((res) => {
      dispatch({
        type: USER_SELECT, //When we dispatch this to the reducer, the switch(type) will determinw which type we are sending for.
        payload: res.data, //The payload needs to be the response data from the server.
      });
    })
    .catch((err) => {
      console.log(err)
      const errors = {
        msg: err.response.data,
        status: err.response.status,
      };
      dispatch({
        type: AUTH_ERROR,
      });
      dispatch({
        type: GET_ERRORS,
        payload: errors,
      });
    });
};



export const changeHotelView = (hotelInfo) => (dispatch) => {
  // This action is for when a client logs in. It returns the token and sets it to local storage, along with the user information


  // 
  const config = {
    headers: {
      "Content-Type": "application/json",
      accept: "application/json",
    },
  };

  const token = localStorage.getItem("token");
  if (token) {
    axios.defaults.headers.common["Authorization"] = `JWT ${token}`
  }

  axios
    .patch("http://localhost:8000/auth/current_user/", hotelInfo, config)
    .then((res) => {
      dispatch({
        type: CHANGE_HOTEL_VIEW, //When we dispatch this to the reducer, the switch(type) will determinw which type we are sending for.
        payload: res.data, // Could be just hotelInfo?    The payload needs to be the response data from the server.
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
