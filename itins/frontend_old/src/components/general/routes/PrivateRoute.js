import React from 'react';
import { Route, Redirect } from 'react-router-dom';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import PropTypes from 'prop-types';
import MainHeader from '../layout/header/MainHeader.js';
import PageHeader from '../layout/header/PageHeader.js';
import items from './RouteHelper.js'

const PrivateRoute = ( {component:Component, auth, routeHelper, ...rest} ) => (
    
    <>   
        <MainHeader/>
        <Route
        {...rest}
        render={props=>{
            if(auth.isLoading) {
                return <h1>Add A Spinner here, with progress...</h1>
    
            } else if(!auth.loggedIn) {
            return <Redirect to={{ 
                pathname: "/login",
                state: {from: props.location}
            }}
            />
    
            } else {
            return (
                <>
                    <PageHeader header={items[routeHelper]['header']} subHeader={items[routeHelper]['subHeader']} icon={items[routeHelper]['pageComponent']}/>
                    <Component {...props}/>
                </>
                )
            }
        }}
        />
    </>
);

PrivateRoute.propTypes = {
  auth: PropTypes.object.isRequired
};


const mapStateToProps = (state) => ({
    auth:state.userReducer,

})

const ShowTheLocationWithRouter = withRouter(PrivateRoute);

export default connect(mapStateToProps)(ShowTheLocationWithRouter);