// src/pages/HomePage.jsx

import React, { useState} from 'react';
import { useSelector } from 'react-redux';
import Header from '../components/ui/Header';
import AnonHomePage from '@/components/homepage/AnonHomepage';
import AgentHomePage from '@/components/homepage/AgentHomePage';
import CustomerHomePage from '@/components/homepage/CustomerHomePage';
import AdminHomePage from '@/components/homepage/AdminHomePage';

const HomePage = () => {
  const user = useSelector((state) => state.auth.user);

  const [selectedLabel, setSelectedLabel] = useState('All');

  const handleLabelSelect = (label) => {
    setSelectedLabel(label);
  };

  return (
    <div>
      <Header onSelectLabel={handleLabelSelect} />
      {user ? (
        user.is_superuser ? (
          <AdminHomePage />
        ) : user.is_agent ? (
          <AgentHomePage selectedLabel={selectedLabel} />
        ) : user.is_customer ? (
          <CustomerHomePage selectedLabel={selectedLabel} />
        ) : (
          <div>Unknown user type</div>
        )
      ) : (
        <AnonHomePage selectedLabel={selectedLabel} />
      )}
    </div>
  );
};
export default HomePage;