import React, { Fragment } from "react";
import LoginForm from "./LoginComponent";
import { useSelector } from "react-redux";
import { Redirect } from "react-router-dom";
import MainHeader from '../general/layout/header/MainHeader';

const Login = ({ location }) => {
  // Assume `isAuthenticated` is part of the state your userReducer manages
  // Adjust the path according to how you've structured your Redux store and slices
const isAuthenticated = useSelector((state) => !!state.auth.token);

  // Redirect logic based on authentication status and the presence of redirect state
  if (isAuthenticated) {
    // If logged in and a redirect path exists in state, redirect there
    // Otherwise, redirect to the home page
    const redirectPath = location.state?.from?.pathname || "/";
    return <Redirect to={redirectPath} />;
  } else {
    // If not authenticated, show the login form
    return (
      <Fragment>
        <MainHeader />
        <br />
        <LoginForm />
      </Fragment>
    );
  }
};

export default Login;
