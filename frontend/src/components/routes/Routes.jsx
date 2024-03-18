import React from 'react';
import { Routes, Route } from "react-router-dom";
import Dashboard from "../../pages/Dashboard";
import LoginComponent from "../../features/auth/components/LoginComponent";
import Subscribe from "../../features/auth/components/Subscribe";

// import PrivateRoute from './PrivateRoute';

const AppRoutes = () => {
  
  return (
      <Routes>
            <Route path="/login" element={<LoginComponent />} />
            <Route path="/" element={<Dashboard />} />
            <Route path="/register" element={<Subscribe />} />  


        {/* <Route element={<PrivateRoute />}>
            This is just for Private Routes Add more private routes here 
        </Route> */}

    </Routes>
  );
};

export default AppRoutes;
