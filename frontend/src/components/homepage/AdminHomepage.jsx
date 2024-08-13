// src/components/homepage/AdminHomePage.jsx

import React from 'react';
import { Button } from "@/components/ui/button";
import AddAgentItinerary from '../itineraries/AddAgentItinerary';
import AddHotel from '../hotels/AddHotel';
import AddAgent from '../users/AddAgent';
import AddComponent from '../components/AddComponent';
import AddPhotos from '../media/AddPhotos';

const AdminHomePage = () => {

  const [activeComponent, setActiveComponent] = React.useState(null);

  const renderComponent = () => {
    switch (activeComponent) {
      case 'AgentItinerary':
        return <AddAgentItinerary />;
      case 'Hotel':
        return <AddHotel />;
      case 'Agent':
        return <AddAgent />;
      case 'Component':
        return <AddComponent />;
      case 'Photos':
        return <AddPhotos />;
      default:
        return null;
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Admin Dashboard</h1>
      <div className="flex space-x-4 mb-6">
        <Button onClick={() => setActiveComponent('AgentItinerary')}>Add Agent Itinerary</Button>
        <Button onClick={() => setActiveComponent('Hotel')}>Add Hotel</Button>
        <Button onClick={() => setActiveComponent('Agent')}>Add Agent</Button>
        <Button onClick={() => setActiveComponent('Component')}>Add Component</Button>
        <Button onClick={() => setActiveComponent('Photos')}>Add Photos</Button>
      </div>
      {renderComponent()}
    </div>
  );
};

export default AdminHomePage;