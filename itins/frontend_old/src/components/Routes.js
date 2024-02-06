import React, { Component, Fragment, useEffect } from "react";
import PrivateRoute from "./general/routes/PrivateRoute.js";

// import { useSelector, useDispatch } from "react-redux";
// import { getBookings } from "../actions/bookings";

import { Switch, Route } from "react-router-dom";
import { withRouter } from "react-router-dom";
// import Alerts from "./general/layout/Alerts.js";
// import items from "./general/routes/RouteHelper.js";
 
const Routes = () => {

    // const dispatch = useDispatch();
    // const default_hotel = useSelector(state => state.userReducer.user? state.userReducer.user.default_hotel:'' );

    // useEffect(() => {  
    //     default_hotel? dispatch(getBookings()):'';
    // }, [default_hotel]);

  return ( 
    <Fragment>
      {/* <Alerts/> */}

      <Switch>
        {/* <PrivateRoute exact path="/bookings" component={BookingsPage} routeHelper='Bookings and Guests'/>
        <PrivateRoute exact path="/" component={Dashboard} routeHelper='Dashboard' />
        <PrivateRoute exact path="/calendar" component={Calendar} routeHelper='Calendar' />
        <PrivateRoute exact path="/settings" component={Settings} routeHelper='Settings and Reports' />

        <Route exact path="/login" component={Login} />

        
                <PrivateRoute exact path="/hotel_management" component ={HotelManagement}/>
                <PrivateRoute exact path="/packages" component ={Packages}/> Products lives inside packages.... as do contacts?
                <PrivateRoute exact path="/tasks" component ={Tasks}/>
                <PrivateRoute exact path="/accounts" component ={Accounts}/>
                <PrivateRoute exact path="/bills" component ={Bills}/>
                <PrivateRoute exact path="/leads" component ={Leads}/> Lives inside Bookings?
                <PrivateRoute exact path="/reports" component ={Reports}/> */}
      </Switch>
    </Fragment>
  );
};

export default withRouter(Routes);
