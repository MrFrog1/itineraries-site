import React from 'react';
import './App.css'
import './index.css'
import { store } from './app/store'
import './assets/fonts.css'
import { Provider } from 'react-redux'
import AppRoutes from "./components/routes/Routes.jsx";
import { BrowserRouter as Router } from "react-router-dom";
import Layout from './components/layout/Layout';
import { useGetHotelsQuery, useGetItinerariesQuery, useGetRegionsQuery } from './services/api';
import LoadingIcon from './components/ui/icons/LoadingIcon'; 

const AppContent = () => {
  const { isLoading: isLoadingHotels } = useGetHotelsQuery();
  const { isLoading: isLoadingItineraries } = useGetItinerariesQuery();
  const { isLoading: isLoadingRegions } = useGetRegionsQuery();

  if (isLoadingHotels || isLoadingItineraries || isLoadingRegions) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="transform scale-[3]"> {/* This increases the size by 300% */}
          <LoadingIcon />
        </div>
      </div>
    );
  }

  return (
    <Layout>
      <div className="App">
        <Router>
          <AppRoutes />
        </Router>
      </div>
    </Layout>
  );
};

function App() {
  return (
    <Provider store={store}>
      <AppContent />
    </Provider>
  )
}

export default App;