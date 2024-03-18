import React from "react";
import Gallery from "../ui/Gallery.jsx";
import { useQuery } from "react-query";
import axios from "axios";

const fetchHotels = async (region) => {
  const response = await axios.get(`/api/hotels?region=${region}`);
  return response.data;
};

const fetchItineraries = async (region) => {
  const response = await axios.get(`/api/itineraries?region=${region}`);
  return response.data;
};

const RegionBoxFinder = ({ region, selectedHeader, hotelItineraryToggle }) => {
  const { data: hotels, isLoading: isHotelsLoading } = useQuery(
    ["hotels", region],
    () => fetchHotels(region),
    { enabled: selectedHeader === "All" || selectedHeader === "Hotels" }
  );

  const { data: itineraries, isLoading: isItinerariesLoading } = useQuery(
    ["itineraries", region],
    () => fetchItineraries(region),
    { enabled: selectedHeader === "All" || selectedHeader === "Itineraries" }
  );

  const isLoading = isHotelsLoading || isItinerariesLoading;

  const filteredData =
    selectedHeader === "All"
      ? hotelItineraryToggle === "Hotels"
        ? hotels
        : itineraries
      : selectedHeader === "Hotels"
      ? hotels
      : itineraries;

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <section className="w-full py-12">
      <div className="container grid gap-6 md:gap-8 px-4 md:px-6">
        <div className="grid grid-cols-1 gap-6">
          {filteredData && filteredData.length > 0 && (
            <div className="flex flex-col gap-1 items-start">
              <h1 className="font-semibold text-blue-600">
                {hotelItineraryToggle} in {region}
              </h1>
              <p className="text-sm leading-none text-gray-600">
                {hotelItineraryToggle === "Hotels"
                  ? "Comfortable stays for your trip."
                  : "Explore the beauty of India."}
              </p>
              <Gallery type={hotelItineraryToggle.toLowerCase()} data={filteredData} />
            </div>
          )}
        </div>
      </div>
    </section>
  );
};

export default RegionBoxFinder;

  // const hotels = [

  //   {
  //     name: "City Lights Inn",
  //     description: "Convenient urban hotel with easy access to attractions and nightlife.",
  //     image: "/static/images/image4.jpg",
  //     price: 3,
  //     rating: 3,
  //   },
  // ];

  // const itineraries = [
  //   {
  //     name: "Historic Sites Tour",
  //     description: "Visit ancient palaces and forts.",
  //     image: "/static/images/image5.jpg",
  //     price: 2,
  //     rating: 4,
  //   }
  // ];