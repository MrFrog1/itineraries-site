import React from 'react';
import { Routes, Route } from "react-router-dom";
import HomePage from "../../pages/HomePage";
import LoginComponent from "../../features/auth/components/LoginComponent";
import Subscribe from "../../features/auth/components/Subscribe";
import AgentProfile from "../../pages/AgentProfile";
import AdminHomePage from '../homepage/AdminHomePage';
import AddHotel from '../hotels/AddHotel';
import AddAgent from '../users/AddAgent';
import ProtectedAdminRoute from './ProtectedAdminRoute';

const AppRoutes = () => {
  
  return (
      <Routes>
            <Route path="/login" element={<LoginComponent />} />
            <Route path="/" element={<HomePage />} />
            <Route path="/register" element={<Subscribe />} />  
            <Route path="/agent_profile" element={<AgentProfile agentId='3' />} />  
          <Route 
            path="/admin" 
            element={
              <ProtectedAdminRoute>
                <AdminHomePage />
              </ProtectedAdminRoute>
            } 
          />
          <Route 
            path="/admin/add-hotel" 
            element={
              <ProtectedAdminRoute>
                <AddHotel />
              </ProtectedAdminRoute>
            } 
          />
          <Route 
            path="/admin/add-agent" 
            element={
              <ProtectedAdminRoute>
                <AddAgent />
              </ProtectedAdminRoute>
            } 
          />
        {/* <Route element={<PrivateRoute />}>
            This is just for Private Routes Add more private routes here 
        </Route> */}

    </Routes>
  );
};

export default AppRoutes;
