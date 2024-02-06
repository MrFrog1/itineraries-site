import React, { Component, Fragment, useEffect } from "react";
import PrivateRoute from "./components/general/routes/PrivateRoute.js";
import HomePage from "./containers/Homepage/HomePage.js";
import BookingsPage from "./bookings/BookingsPage.js";
import Login from "./components/login/Login.js";
import { useSelector, useDispatch } from "react-redux";
import { getBookings } from "../actions/bookings";

import Calendar from "./bookings/Calendar.js";

import Settings from "./settings/Settings.js";
import { Switch, Route } from "react-router-dom";
import { withRouter } from "react-router-dom";
import Alerts from "./components/general/layout/Alerts.js";
import items from "./components/general/routes/RouteHelper.js";
 
const Routes = () => {

    const dispatch = useDispatch();
    const default_hotel = useSelector(state => state.userReducer.user? state.userReducer.user.default_hotel:'' );

    useEffect(() => {  
        default_hotel? dispatch(getBookings()):'';
    }, [default_hotel]);

  return ( 
    <Fragment>
      {/* <Alerts/> */}

      <Switch>
        <PrivateRoute exact path="/bookings" component={BookingsPage} routeHelper='Bookings and Guests'/>
        <PrivateRoute exact path="/" component={HomePage} routeHelper='HomePage' />
        <PrivateRoute exact path="/calendar" component={Calendar} routeHelper='Calendar' />
        <PrivateRoute exact path="/settings" component={Settings} routeHelper='Settings and Reports' />

        <Route exact path="/login" component={Login} />

      </Switch>
    </Fragment>
  );
};

export default withRouter(Routes);


