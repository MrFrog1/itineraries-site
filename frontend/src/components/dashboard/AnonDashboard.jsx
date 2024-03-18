// AnonDashboard.jsx
import React, { useState } from 'react';
import IndiaMap from './IndiaMap';
import RegionList from './RegionList';
import { Badge } from "@/components/ui/badge";
import WeeklyHotelsAndItineraries from './WeeklyHotelsAndItineraries';
import { useGetRegionsQuery } from '../../services/api';

const AnonDashboard = ({ selectedLabel }) => {
  const [weatherMode, setWeatherMode] = useState(false);
  const [selectedMonth, setSelectedMonth] = useState(null);
  const [hoveredRegion, setHoveredRegion] = useState(null);
  const [selectedMapRegion, setSelectedMapRegion] = useState(null);
  const [showMonthDropdown, setShowMonthDropdown] = useState(false);

   const { data: regions, isLoading, error } = useGetRegionsQuery();
 
  const handleWeatherToggle = () => {
    setWeatherMode(!weatherMode);
    setShowMonthDropdown(!showMonthDropdown);
    if (!weatherMode) {
      setSelectedMonth(null);
    }
  };

  const handleMonthSelect = (month) => {
    setSelectedMonth(month);
    setShowMonthDropdown(false);
  };

  const handleRegionHover = (region) => {
    console.log(region);
    setHoveredRegion(region);
  };

  const handleRegionClick = (regionName) => {
    setSelectedMapRegion(regionName);
  };

  const handleMapRegionSelect = (region) => {
    setSelectedMapRegion(region);
  };

  return (
    <div>
      <div className="grid grid-cols-12 gap-8">
        <section className="col-span-5">
          <div className="my-8">
            <div className="relative mb-4 ml-80">
              <Badge
                className="bg-white-500 text-black px-4 py-2 rounded"
                onClick={handleWeatherToggle}
              >
                {weatherMode ? (
                  <>
                    Weather: {selectedMonth || 'Select Month'}
                    <span
                      className="ml-2 cursor-pointer"
                      onClick={() => {
                        setWeatherMode(false);
                        setSelectedMonth(null);
                      }}
                    >
                      ×
                    </span>
                  </>
                ) : (
                  'Weather'
                )}
              </Badge>
              {showMonthDropdown && (
                <div className="absolute mt-2 py-2 w-48 bg-white rounded-md shadow-xl z-20">
                  {['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'].map((month) => (
                    <Badge
                      key={month}
                      className="block bg-white px-4 py-2 text-gray-800 hover:bg-gray-200"
                      onClick={() => handleMonthSelect(month)}
                    >
                      {month}
                    </Badge>
                  ))}
                </div>
              )}
            </div>
            <IndiaMap
              onRegionClick={handleRegionClick}
              onRegionSelect={handleMapRegionSelect}
              weatherMode={weatherMode}
              selectedMonth={selectedMonth}
              onRegionHover={handleRegionHover}
              hoveredRegion={hoveredRegion}
              selectedLabel={selectedLabel}
            />
          </div>
        </section>
        <section className="col-span-7">
          <div className="my-8">
            <RegionList
              onRegionHover={handleRegionHover}
              selectedLabel={selectedLabel}
              selectedMapRegion={selectedMapRegion}
              weatherMode={weatherMode}
            />
          </div>
        </section>
      </div>
      <div className="my-12">
        <hr className="w-4/5 mx-auto border-t border-gray-300" />
      </div>
      <section>
        <WeeklyHotelsAndItineraries selectedLabel={selectedLabel} />
      </section>
      <div className="my-12">
        <hr className="w-4/5 mx-auto border-t border-gray-300" />
      </div>
    </div>
  );
};

export default AnonDashboard;