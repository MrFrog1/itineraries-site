import React, { useState } from 'react';
import { useSelector } from 'react-redux';
import Header from '../components/ui/Header';
import AgentDashboard from '../components/dashboard/AgentDashboard';
import CustomerDashboard from '../components/dashboard/CustomerDashboard';
import AnonDashboard from '../components/dashboard/AnonDashboard';
import AgentGallery from '../components/dashboard/AgentGallery';


const Dashboard = () => {
  const user = useSelector((state) => state.auth.user);
  const [selectedLabel, setSelectedLabel] = useState('All');

  const handleLabelSelect = (label) => {
    setSelectedLabel(label);
  };

 return (
    <div>
      <Header onSelectLabel={handleLabelSelect} />
      {user ? (
        user.is_agent ? (
          <AgentDashboard selectedLabel={selectedLabel} />
        ) : user.is_customer ? (
          <>
            <CustomerDashboard selectedLabel={selectedLabel} />
            <section>
              <h2 className="text-4xl text-center font-montserrat mb-4">Experts</h2>
              <AgentGallery />
            </section>
          </>
        ) : null
      ) : (
        <>
          <AnonDashboard selectedLabel={selectedLabel} />
          <section>
            <h2 className="text-4xl text-center font-montserrat mb-4">Experts</h2>
            <AgentGallery />
          </section>
        </>
      )}
    </div>
  );
};

export default Dashboard;