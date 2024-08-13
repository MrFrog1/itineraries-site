import React from "react";
import Gallery from "../ui/Gallery.jsx";
import { useGetHotelsQuery, useGetItinerariesQuery, useGetHotelPhotosQuery, useGetItineraryPhotosQuery } from '../../services/api.js/index.js';

const RegionBoxFinder = ({ region, selectedHeader, hotelItineraryToggle }) => {
  const { data: hotels, isLoading: isHotelsLoading } = useGetHotelsQuery();
  const { data: itineraries, isLoading: isItinerariesLoading } = useGetItinerariesQuery();

  // Fetch hotel photos
  const { data: hotelPhotos, isLoading: isHotelPhotosLoading } = useGetHotelPhotosQuery(
    hotels?.map((hotel) => hotel.id),
    {
      skip: !hotels || hotels.length === 0,
    }
  );

  // Fetch itinerary photos
  const { data: itineraryPhotos, isLoading: isItineraryPhotosLoading } = useGetItineraryPhotosQuery(
    itineraries?.map((itinerary) => itinerary.id),
    {
      skip: !itineraries || itineraries.length === 0,
    }
  );

  // Combine hotel and itinerary data with their respective photos
  const hotelsWithPhotos = hotels?.map((hotel) => ({
    ...hotel,
    photos: hotelPhotos?.filter((photo) => photo.hotel === hotel.id),
  }));

  const itinerariesWithPhotos = itineraries?.map((itinerary) => ({
    ...itinerary,
    photos: itineraryPhotos?.filter((photo) => photo.itinerary === itinerary.id),
  }));

  const filteredData =
    selectedHeader === "All"
      ? hotelItineraryToggle === "Hotels"
        ? hotelsWithPhotos
        : itinerariesWithPhotos
      : selectedHeader === "Hotels"
      ? hotelsWithPhotos
      : itinerariesWithPhotos;

  if (isHotelsLoading || isItinerariesLoading || isHotelPhotosLoading || isItineraryPhotosLoading) {
    return <div>Loading...</div>;
  }

  const headerText = selectedHeader === "All" ? hotelItineraryToggle : selectedHeader;
  const descriptionText =
    selectedHeader === "All"
      ? hotelItineraryToggle === "Hotels"
        ? "Comfortable stays for your trip."
        : "Explore the beauty of India."
      : selectedHeader === "Hotels"
      ? "Comfortable stays for your trip."
      : "Explore the beauty of India.";

  return (
    <section className="w-full py-12">
      <div className="container grid gap-6 md:gap-8 px-4 md:px-6">
        <div className="grid grid-cols-1 gap-6">
          {filteredData && filteredData.length > 0 && (
            <div className="flex flex-col gap-1 items-start">
              <h1 className="font-semibold text-blue-600">
                {headerText} in {region}
              </h1>
              <p className="text-sm leading-none text-gray-600">{descriptionText}</p>
              <Gallery data={filteredData} />
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