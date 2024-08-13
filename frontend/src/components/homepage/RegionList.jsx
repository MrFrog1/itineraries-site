import { Link } from "react-router-dom";
import React, { useMemo, useState, useEffect } from "react";
import RegionBoxFinder from "./RegionBoxFinder";

export default function RegionList({ onRegionHover, selectedLabel, selectedMapRegion, weatherMode }) {
  const [selectedRegion, setSelectedRegion] = useState("Ladakh");

  // console.log(selectedLabel)
  const handleRegionClick = (region) => {
    setSelectedRegion(region);
  };


  useEffect(() => {
    if (selectedMapRegion) {
      setSelectedRegion(selectedMapRegion);
    }
  }, [selectedMapRegion]);




  const regions = useMemo(
    () => [
      { name: "Ladakh", description: "Land of high passes." },
      { name: "Rajasthan", description: "The land of kings." },
      { name: "Kashmir", description: "The paradise on Earth." },
      { name: "Madhya Pradesh", description: "The heart of India." },
    ],
    []
  );

  return (
    <div className="w-full overflow-hidden">
      <section className="w-full py-9">
        <div className="container grid gap-6 md:gap-8 px-4 md:px-6">
          <div className="flex justify-center mt-4">
            <h2 className="text-5xl font-bold ml-20">Local</h2>
          </div>
          <div className="flex justify-around mt-4">
            <span className="text-3xl font-montserrat font-light">Agents</span>
            <span className="text-3xl font-montserrat font-light">Rates</span>
            <span className="text-3xl font-montserrat font-light">Hotels</span>
            <span className="text-3xl font-montserrat font-light">Knowledge</span>
          </div>
          <div className="flex justify-center mt-4">
            <h2 className="text-4xl font-semibold ml-20">Highly Personal Stays and Itineraries </h2>
          </div>
          <div className="grid grid-cols-[30%_70%] gap-6 mt-12">
            <div className="flex flex-col gap-10 ml-12">
              {regions.map((region, index) => (
                <div
                  key={index}
                  className="flex items-center cursor-pointer"
                  onClick={() => handleRegionClick(region.name)}
                  onMouseEnter={() => {
                    onRegionHover(region.name);
                    if (weatherMode) {
                      onRegionHover(region.name);
                    }
                  }}
                  onMouseLeave={() => {
                    onRegionHover(null);
                  }}
                >
                  <h3
                    className={`text-xl font-semibold ${
                      selectedRegion === region.name ? "text-black" : "text-[#A7252A]"
                    }`}
                  >
                    {region.name}
                  </h3>
                </div>
              ))}
            </div>
            <div>
              {selectedRegion && (
                <RegionBoxFinder region={selectedRegion} selectedHeader={selectedLabel} />
              )}
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

