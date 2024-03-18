import React from 'react';
import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useSelector } from 'react-redux';
import Header from '../ui/Header'; // Import your Header component

const PrivateRoute = () => {
    const location = useLocation();
    const { isAuthenticated } = useSelector((state) => state.auth); // Adjust based on your auth slice

    if (!isAuthenticated) {
        // Redirect to login page, but save the current location they were trying to go to
        return <Navigate to="/login" state={{ from: location }} replace />;
    }

    return (
        <>
            <Header /> {/* Render the Header */}
            <Outlet /> {/* Render child routes */}
        </>
    );
};

export default PrivateRoute;