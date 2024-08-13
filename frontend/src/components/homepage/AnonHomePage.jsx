import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { useGetHotelsQuery, useGetItinerariesQuery } from '../../services/api';
import SearchBox from './SearchBox';
import Gallery from './Gallery';
import { ChevronDownIcon, ChevronUpIcon } from '../ui/icons';

const AnonHomePage = () => {
  const dispatch = useDispatch();
  const { data: hotels, isLoading: hotelsLoading } = useGetHotelsQuery();
  const { data: itineraries, isLoading: itinerariesLoading } = useGetItinerariesQuery();

  const [searchParams, setSearchParams] = useState({
    activeTab: 'hotels',
    location: '',
    type: '',
    minPrice: '',
    maxPrice: '',
    hoursFrom: '',
    hoursMode: 'driving',
    selectedButtons: [],
    month: '',
    bestFor: '',
  });

  const [isSearchBoxCollapsed, setIsSearchBoxCollapsed] = useState(false);

  const handleSearchChange = (newParams) => {
    setSearchParams(prevParams => ({ ...prevParams, ...newParams }));
  };

  const toggleSearchBox = () => {
    setIsSearchBoxCollapsed(!isSearchBoxCollapsed);
  };

  return (
    <div className="flex flex-col lg:flex-row min-h-screen bg-white">
      <div className="lg:w-[35%] p-4">
        <div className="lg:hidden flex justify-between items-center mb-4" onClick={toggleSearchBox}>
          <h2 className="text-lg font-semibold">Search</h2>
          {isSearchBoxCollapsed ? <ChevronDownIcon size={24} /> : <ChevronUpIcon size={24} />}
        </div>
        <div className={`${isSearchBoxCollapsed ? 'hidden' : 'block'} lg:block`}>
          <SearchBox searchParams={searchParams} onSearchChange={handleSearchChange} />
        </div>
      </div>
      <div className="lg:w-[65%] overflow-y-auto">
        <Gallery 
          hotels={hotels} 
          itineraries={itineraries} 
          isLoading={hotelsLoading || itinerariesLoading}
          searchParams={searchParams}
        />
      </div>
    </div>
  );
};

export default AnonHomePage;

// src/components/dashboard/AnonHomePage.jsx

// import React, { useState, useEffect } from 'react';
// import { useDispatch, useSelector } from 'react-redux';
// import { useGetHotelsQuery, useGetItinerariesQuery, useGetRegionsQuery } from '../../services/api';
// import SearchBox from './SearchBox';
// import Gallery from './Gallery';

// const AnonHomePage = () => {
//   const dispatch = useDispatch();
//   const [activeTab, setActiveTab] = useState('hotels');
//   const [searchParams, setSearchParams] = useState({
//     regions: [],
//     types: [],
//     priceRange: [],
//     tags: [],
//     hoursFrom: null,
//     travelMode: 'driving'
//   });

//   const { data: hotels, isLoading: isLoadingHotels } = useGetHotelsQuery(searchParams);
//   const { data: itineraries, isLoading: isLoadingItineraries } = useGetItinerariesQuery(searchParams);
//   const { data: regions, isLoading: isLoadingRegions } = useGetRegionsQuery();

//   const handleSearchChange = (newParams) => {
//     setSearchParams(prev => ({ ...prev, ...newParams }));
//   };

//   const displayData = activeTab === 'hotels' ? hotels : itineraries;
//   const isLoading = activeTab === 'hotels' ? isLoadingHotels : isLoadingItineraries;

//   return (
//     <div className="flex flex-col md:flex-row h-screen">
//       <div className="w-full md:w-1/3 p-4">
//         <SearchBox
//           activeTab={activeTab}
//           setActiveTab={setActiveTab}
//           regions={regions}
//           onSearchChange={handleSearchChange}
//           searchParams={searchParams}
//         />
//       </div>
//       <div className="w-full md:w-2/3 p-4">
//         <Gallery data={displayData} isLoading={isLoading} />
//       </div>
//     </div>
//   );
// };

// export default AnonHomePage;




// // AnonDashboard.jsx
// import RegionList from './RegionList';
// import { Badge } from "@/components/ui/badge";
// import WeeklyHotelsAndItineraries from './WeeklyHotelsAndItineraries';
// import { useGetRegionsQuery } from '../../services/api';
// import { LoadingIcon} from '../ui/icons';


// const AnonDashboard = ({ selectedLabel }) => {
//   const [weatherMode, setWeatherMode] = useState(false);
//   const [selectedMonth, setSelectedMonth] = useState(null);
//   const [hoveredRegion, setHoveredRegion] = useState(null);
//   const [selectedMapRegion, setSelectedMapRegion] = useState(null);
//   const [showMonthDropdown, setShowMonthDropdown] = useState(false);

//    const { data: regions, isLoading, error } = useGetRegionsQuery();
 
//   const handleWeatherToggle = () => {
//     setWeatherMode(!weatherMode);
//     setShowMonthDropdown(!showMonthDropdown);
//     if (!weatherMode) {
//       setSelectedMonth(null);
//     }
//   };

//   const handleMonthSelect = (month) => {
//     setSelectedMonth(month);
//     setShowMonthDropdown(false);
//   };

//   const handleRegionHover = (region) => {
//     console.log(region);
//     setHoveredRegion(region);
//   };

//   const handleRegionClick = (regionName) => {
//     setSelectedMapRegion(regionName);
//   };

//   const handleMapRegionSelect = (region) => {
//     setSelectedMapRegion(region);
//   };

//   if (isLoading) {
//     return <div>Loading...</div>;
//   }

//   if (error) {
//     return <div>Error: {error.message}</div>;
//   }


//   return (
//     <div>
//       <LoadingIcon/>
//       <div className="grid grid-cols-12 gap-8">
//         <section className="col-span-5">
//           <div className="my-8">
//             <div className="relative mb-4 ml-80">
//               <Badge
//                 className="bg-white-500 text-black px-4 py-2 rounded"
//                 onClick={handleWeatherToggle}
//               >
//                 {weatherMode ? (
//                   <>
//                     Weather: {selectedMonth || 'Select Month'}
//                     <span
//                       className="ml-2 cursor-pointer"
//                       onClick={() => {
//                         setWeatherMode(false);
//                         setSelectedMonth(null);
//                       }}
//                     >
//                       ×
//                     </span>
//                   </>
//                 ) : (
//                   'Weather'
//                 )}
//               </Badge>
//               {showMonthDropdown && (
//                 <div className="absolute mt-2 py-2 w-48 bg-white rounded-md shadow-xl z-20">
//                   {['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'].map((month) => (
//                     <Badge
//                       key={month}
//                       className="block bg-white px-4 py-2 text-gray-800 hover:bg-gray-200"
//                       onClick={() => handleMonthSelect(month)}
//                     >
//                       {month}
//                     </Badge>
//                   ))}
//                 </div>
//               )}
//             </div>
//             <IndiaMap
//               onRegionClick={handleRegionClick}
//               onRegionSelect={handleMapRegionSelect}
//               weatherMode={weatherMode}
//               selectedMonth={selectedMonth}
//               onRegionHover={handleRegionHover}
//               hoveredRegion={hoveredRegion}
//               selectedLabel={selectedLabel}
//               regions={regions}
//             />
//           </div>
//         </section>
//         <section className="col-span-7">
//           <div className="my-8">
//             <RegionList
//               onRegionHover={handleRegionHover}
//               selectedLabel={selectedLabel}
//               selectedMapRegion={selectedMapRegion}
//               weatherMode={weatherMode}
//             />
//           </div>
//         </section>
//       </div>
//       <div className="my-12">
//         <hr className="w-4/5 mx-auto border-t border-gray-300" />
//       </div>
//       <section>
//         <WeeklyHotelsAndItineraries selectedLabel={selectedLabel} />
//       </section>
//       <div className="my-12">
//         <hr className="w-4/5 mx-auto border-t border-gray-300" />
//       </div>
//     </div>
//   );
// };

// export default AnonDashboard;