import { Button } from "@/components/ui/button";
import React, { memo, useState, useEffect } from "react";
import { Badge } from "@/components/ui/badge";
import { LoadingPlaceholder, ChevronLeftIcon, ChevronRightIcon, StarIcon, AppleIcon, BirdIcon, TreesIcon, InstagramIcon, CastleIcon, CircleIcon, MountainIcon, TractorIcon} from '../ui/icons';
  
// Simulated data for hotels and itineraries

  const hotelData = [
    {
        id: 1,
        name: "Grand View Hotel",
        description: "Stunning beachfront hotel with panoramic ocean views.",
        longDescription: "Experience luxury and relaxation at our stunning beachfront hotel. Enjoy breathtaking panoramic views of the ocean from every room.",
        image: "/static/images/image1.jpg",
        region: "Goa",
        price: 4,
        category:"Wellness",
        rating: 4,
        base_price_for_2p: 10000,
        instagram_link: "www.instagaram.com/indusrivercamp",
    },
    {
        id: 2,
        name: "Tranquil Oasis Resort",
        description: "Luxurious spa retreat nestled in a serene tropical paradise.",
        longDescription: "Experience luxury and relaxation at our stunning beachfront hotel. Enjoy breathtaking panoramic views of the ocean from every room.",
        region: "Ladakh",
        image: "/static/images/image2.jpg",
        price: 5,
        category:"Food Stays",
        rating: 5,
        base_price_for_2p: 25000,
        instagram_link: "www.instagaram.com/indusrivercamp",

    },
    {
        id: 3,
        name: "Mountain Vista Lodge",
        description: "Cozy alpine hotel offering breathtaking views of the mountains.",
        longDescription: "Experience luxury and relaxation at our stunning beachfront hotel. Enjoy breathtaking panoramic views of the ocean from every room.",
        region: "Ladakh",
        image: "/static/images/port.jpg",
        price: 4,
        rating: 4,
        category:"Wildlife",
        base_price_for_2p: 1500,
        instagram_link: "www.instagaram.com/indusrivercamp"

    },
    {
        id: 4,
        name: "City Lights Inn",
        description: "Convenient urban hotel with easy access to attractions and nightlife.",
        longDescription: "Experience luxury and relaxation at our stunning beachfront hotel. Enjoy breathtaking panoramic views of the ocean from every room.",
        region: "Ladakh",
        image: "/static/images/image4.jpg",
        price: 3,
        rating: 3,
        category:"Wildlife",
        base_price_for_2p: 28000,
        instagram_link: "www.instagaram.com/indusrivercamp"

    },
  ];

  const itineraryData = [
    {
        id: 1,
        name: "Historic Sites Tour",
        description: "Visit ancient palaces and forts.",
        longDescription: "Embark on a journey through time as you explore the ancient palaces and forts of Rajasthan. Discover the rich history and culture of this fascinating region.",
        image: "/static/images/image5.jpg",
        region: "Rajasthan",
        price: 2,
        rating: 4,
        category:"Birding",
        days: 14,
        price_per_couple: 100000,
    },
    {
        id: 2,
        name: "Nature Walk",
        description: "Explore the beauty of the Himalayas.",
        longDescription: "Embark on a journey through time as you explore the ancient palaces and forts of Rajasthan. Discover the rich history and culture of this fascinating region.",
        region: "Rajasthan",
        image: "/static/images/image2.jpg",
        price: 1,
        rating: 5,
        category:"Cultural Immersion",
        days: 5,
        price_per_couple: 60000,
    },
    {
        id: 3,
        name: "Wildlife Safari",
        description: "Spot tigers and elephants in the jungle.",
        longDescription: "Embark on a journey through time as you explore the ancient palaces and forts of Rajasthan. Discover the rich history and culture of this fascinating region.",
        region: "Kashmir",
        image: "/static/images/image3.jpg",
        price: 3,
        rating: 4,
        category:"Farmstays",
        days: 8,
        price_per_couple: 65000,
    },
    {
        id: 4,
        name: "IRC Safari",
        description: "Mountains and .... .",
        longDescription: "Embark on a journey through time as you explore the ancient palaces and forts of Rajasthan. Discover the rich history and culture of this fascinating region.",
        region: "Kerala",
        image: "/static/images/image1.jpg",
        price: 3,
        rating: 4,
        category:"Heritage Hotels",
        days: 44,
        price_per_couple: 300000,
    },
  ];


function WeeklyHotelsAndItineraries({ selectedLabel }) {
  const [hotels, setHotels] = useState([]);
  const [itineraries, setItineraries] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [currentHotelIndex, setCurrentHotelIndex] = useState(0);
  const [currentItineraryIndex, setCurrentItineraryIndex] = useState(0);
  const [selectedCategories, setSelectedCategories] = useState([]);

  useEffect(() => {
    // Simulated API call to fetch hotels and itineraries
    const fetchData = async () => {
      setIsLoading(true);
      await new Promise((resolve) => setTimeout(resolve, 1000));
      setHotels(hotelData);
      setItineraries(itineraryData);
      setIsLoading(false);
    };

    fetchData();
  }, []);

  const handleHotelPrev = () => {
    setCurrentHotelIndex((prevIndex) => (prevIndex === 0 ? hotels.length - 3 : prevIndex - 1));
  };

  const handleHotelNext = () => {
    setCurrentHotelIndex((prevIndex) => (prevIndex === hotels.length - 3 ? 0 : prevIndex + 1));
  };

  const handleItineraryPrev = () => {
    setCurrentItineraryIndex((prevIndex) => (prevIndex === 0 ? itineraries.length - 3 : prevIndex - 1));
  };

  const handleItineraryNext = () => {
    setCurrentItineraryIndex((prevIndex) => (prevIndex === itineraries.length - 3 ? 0 : prevIndex + 1));
  };

  const toggleCategory = (category) => {
    if (selectedCategories.includes(category)) {
      setSelectedCategories(selectedCategories.filter((cat) => cat !== category));
    } else {
      setSelectedCategories([...selectedCategories, category]);
    }
  };

  const filteredHotels = hotels.filter((hotel) =>
    selectedCategories.length === 0 ? true : selectedCategories.includes(hotel.category)
  );

  const filteredItineraries = itineraries.filter((itinerary) =>
    selectedCategories.length === 0 ? true : selectedCategories.includes(itinerary.category)
  );

  const displayedHotels = filteredHotels.slice(currentHotelIndex, currentHotelIndex + 3);
  const displayedItineraries = filteredItineraries.slice(currentItineraryIndex, currentItineraryIndex + 3);

  return (
    <div className="flex flex-col items-center py-12 bg-white">
      <h2 className="text-4xl font-montserrat mb-4">Our Top Picks</h2>
      <div className="mt-4 mb-8">
        <div className="grid grid-cols-8 gap-4">
          {/* Category filter icons */}
          <div
            className={`flex flex-col items-center space-y-1 cursor-pointer ${
              selectedCategories.includes("Food Stays") ? "text-blue-500" : "text-gray-500"
            }`}
            onClick={() => toggleCategory("Food Stays")}
          >
            <AppleIcon className="h-6 w-6" />
            <p className="text-xs">Food Stays</p>
          </div>
          <div
            className={`flex flex-col items-center space-y-1 cursor-pointer ${
              selectedCategories.includes("Wildlife") ? "text-blue-500" : "text-gray-500"
            }`}
            onClick={() => toggleCategory("Wildlife")}
          >
            <BirdIcon className="h-6 w-6" />
            <p className="text-xs">Wildlife</p>
          </div>
          <div
            className={`flex flex-col items-center space-y-1 cursor-pointer ${
              selectedCategories.includes("Birding") ? "text-blue-500" : "text-gray-500"
            }`}
            onClick={() => toggleCategory("Birding")}
          >
            <BirdIcon className="h-6 w-6" />
            <p className="text-xs">Birding</p>
          </div>
          <div
            className={`flex flex-col items-center space-y-1 cursor-pointer ${
              selectedCategories.includes("Stay in Nature") ? "text-blue-500" : "text-gray-500"
            }`}
            onClick={() => toggleCategory("Stay in Nature")}
          >
            <TreesIcon className="h-6 w-6" />
            <p className="text-xs">Stay in Nature</p>
          </div>
          <div
            className={`flex flex-col items-center space-y-1 cursor-pointer ${
              selectedCategories.includes("Wellness") ? "text-blue-500" : "text-gray-500"
            }`}
            onClick={() => toggleCategory("Wellness")}
          >
            <MountainIcon className="h-6 w-6" />
            <p className="text-xs">Wellness</p>
          </div>
          <div
            className={`flex flex-col items-center space-y-1 cursor-pointer ${
              selectedCategories.includes("Cultural Immersion") ? "text-blue-500" : "text-gray-500"
            }`}
            onClick={() => toggleCategory("Cultural Immersion")}
          >
            <CircleIcon className="h-6 w-6" />
            <p className="text-xs">Cultural Immersion</p>
          </div>
          <div
            className={`flex flex-col items-center space-y-1 cursor-pointer ${
              selectedCategories.includes("Farmstays") ? "text-blue-500" : "text-gray-500"
            }`}
            onClick={() => toggleCategory("Farmstays")}
          >
            <TractorIcon className="h-6 w-6" />
            <p className="text-xs">Farmstays</p>
          </div>
          <div
            className={`flex flex-col items-center space-y-1 cursor-pointer ${
              selectedCategories.includes("Heritage Hotels") ? "text-blue-500" : "text-gray-500"
            }`}
            onClick={() => toggleCategory("Heritage Hotels")}
          >
            <CastleIcon className="h-6 w-6" />
            <p className="text-xs">Heritage Hotels</p>
          </div>
        </div>
      </div>
      {selectedLabel === "All" || selectedLabel === "Hotels" ? (
        <section className="mb-12">
          {isLoading ? (
            <LoadingPlaceholder />
          ) : displayedHotels.length === 0 ? (
            <p className="text-lg text-gray-600">No hotels match the selected categories.</p>
          ) : (
            <div className="flex max-w-6xl space-x-8">
              <div className="flex items-center" style={{ marginTop: "-130px" }}>
                <div className="w-10 h-10 rounded-full bg-[#EBE8E2] flex items-center justify-center">
                  <ChevronLeftIcon className="my-auto text-black cursor-pointer" onClick={handleHotelPrev} />
                </div>
              </div>
              <div className="grid grid-cols-3 gap-8">
                {displayedHotels.map((hotel) => (
                  <div key={hotel.id} className="flex flex-col items-center space-y-4">
                    <div className="relative">
                      <img
                        alt={hotel.name}
                        className="h-[300px] w-[300px] rounded-lg object-cover"
                        height="300"
                        src={hotel.image}
                        style={{ aspectRatio: "300/300", objectFit: "cover" }}
                        width="300"
                      />
                      <div className="absolute inset-0 flex items-center justify-center opacity-0 hover:opacity-100 bg-black bg-opacity-50 transition duration-300">
                        <div className="text-white text-center p-4">
                          <p>{hotel.longDescription}</p>
                        </div>
                      </div>
                    </div>
                    <h3 className="text-lg font-semibold">{hotel.name}</h3>
                    <p className="text-sm text-gray-600">{hotel.description}</p>
                    <p className="text-sm text-gray-600">Region: {hotel.region}</p>
                    <div className="flex items-center space-x-2">
                      <a href={hotel.instagram_link} target="_blank" rel="noopener noreferrer">
                        <InstagramIcon className="h-5 w-5 text-gray-500 hover:text-pink-500" />
                      </a>
                      <p className="text-sm text-gray-600">
                        From {formatPrice(hotel.base_price_for_2p)} per night for 2 people
                      </p>
                    </div>
                    <div className="flex items-center">
                      {Array(5)
                        .fill()
                        .map((_, index) => (
                          <StarIcon
                            key={index}
                            className={`h-4 w-4 ${index < hotel.rating ? "text-yellow-500" : "text-gray-300"}`}
                          />
                        ))}
                    </div>
                    <Button variant="outline">Learn More</Button>
                  </div>
                ))}
              </div>
              <div className="flex items-center" style={{ marginTop: "-130px" }}>
                <div className="w-10 h-10 rounded-full bg-[#EBE8E2] flex items-center justify-center">
                  <ChevronRightIcon className="my-auto text-black cursor-pointer" onClick={handleHotelNext} />
                </div>
              </div>
            </div>
          )}
        </section>
      ) : null}
      {selectedLabel === "All" || selectedLabel === "Itineraries" ? (
        <section>
          {isLoading ? (
            <LoadingPlaceholder />
          ) : displayedItineraries.length === 0 ? (
            <p className="text-lg text-gray-600">No itineraries match the selected categories.</p>
          ) : (
            <div className="flex max-w-6xl space-x-8">
              <div className="flex items-center" style={{ marginTop: "-130px" }}>
                <div className="w-10 h-10 rounded-full bg-[#EBE8E2] flex items-center justify-center">
                  <ChevronLeftIcon className="my-auto text-black cursor-pointer" onClick={handleItineraryPrev} />
                </div>
              </div>
              <div className="grid grid-cols-3 gap-8">
                {displayedItineraries.map((itinerary) => (
                  <div key={itinerary.id} className="flex flex-col items-center space-y-4">
                    <div className="relative">
                      <img
                        alt={itinerary.name}
                        className="h-[300px] w-[300px] rounded-lg object-cover"
                        height="300"
                        src={itinerary.image}
                        style={{ aspectRatio: "300/300", objectFit: "cover" }}
                        width="300"
                      />
                      <div className="absolute inset-0 flex items-center justify-center opacity-0 hover:opacity-100 bg-black bg-opacity-50 transition duration-300">
                        <div className="text-white text-center p-4">
                          <p>{itinerary.longDescription}</p>
                        </div>
                      </div>
                    </div>
                    <h3 className="text-lg font-semibold">{itinerary.name}</h3>
                    <p className="text-sm text-gray-600">{itinerary.description}</p>
                    <p className="text-sm text-gray-600">Region: {itinerary.region}</p>
                    <div className="flex flex-col items-center space-y-1">
                      <p className="text-sm text-gray-600">A {itinerary.days} days itinerary</p>
                      <p className="text-sm text-gray-600">
                        Approximate pricing at {formatPrice(itinerary.price_per_couple)} per couple
                      </p>
                    </div>
                    <Button variant="outline">Learn More</Button>                  </div>
                ))}
              </div>
              <div className="flex items-center" style={{ marginTop: "-130px" }}>
                <div className="w-10 h-10 rounded-full bg-[#EBE8E2] flex items-center justify-center">
                  <ChevronRightIcon className="my-auto text-black cursor-pointer" onClick={handleItineraryNext} />
                </div>
              </div>
            </div>
          )}
        </section>
      ) : null}
    </div>
  );
}

export default memo(WeeklyHotelsAndItineraries)



function formatPrice(price) {
  return price.toLocaleString("en-IN", {
    style: "currency",
    currency: "INR",
    minimumFractionDigits: 0,
  });
}