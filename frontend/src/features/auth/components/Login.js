import React, { Fragment } from "react";
import LoginForm from "./LoginComponent.js";
// import SignUp from './SignUp.js';
import { useSelector } from "react-redux";
import { Redirect } from "react-router";
import MainHeader from '../general/layout/header/MainHeader.js';

const Login = (props) => {
  const userReducer = useSelector((state) => state.userReducer);

  if (userReducer.loggedIn && !props.location.state) {
    return <Redirect to="/" />;
  } else if (userReducer.loggedIn && props.location.state) {
    return <Redirect to={props.location.state.from.pathname} />;
  } else {
    return (
      <Fragment>
        <MainHeader/>
        <br></br>
        <LoginForm />
      </Fragment>
    );
  }
};

export default Login;
