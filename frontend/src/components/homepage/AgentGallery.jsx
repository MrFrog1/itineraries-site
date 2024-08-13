// make fetchExperts and fixed Date Departures. 
import { Button } from "@/components/ui/button";
import { useEffect, useState } from "react";
import { LoadingPlaceholder, ChevronLeftIcon, ChevronRightIcon} from '../ui/icons';


const agentData = [
  {
    id: 1,
    name: "Mrs Frog",
    description: "A British-Dutch concert pianist.",
    photo: "/static/images/portrait1.jpg",
    primaryRegions: ["Ladakh", "Rajasthan"],
    fixedDateDepartures: ["15th July", "20th August"],
  },
  {
    id: 2,
    name: "Mr Mcvities",
    description: "Pioneering watchmaker and time historian.",
    photo: "/static/images/portrait2.jpg",
    primaryRegions: ["Delhi", "Sikkim"],
    fixedDateDepartures: [],
  },
  {
    id: 3,
    name: "Colonel Kentucky",
    description: "Award-winning photographer.",
    photo: "/static/images/portrait3.jpg",
    primaryRegions: ["Region 1"],
    fixedDateDepartures: ["2023-09-10"],
  },
  {
    id: 4,
    name: "Sir Michael",
    description: "Award-winning photographer.",
    photo: "/static/images/portrait4.jpg",
    primaryRegions: ["North East"],
    fixedDateDepartures: ["2023-09-10"],
  },
  {
    id: 5,
    name: "Lady Lavender",
    description: "Experienced yoga instructor and wellness coach.",
    photo: "/static/images/portrait5.jpg",
    primaryRegions: ["Goa", "Kerala"],
    fixedDateDepartures: ["2023-11-15"],
  },
  {
    id: 6,
    name: "Dr. Dolittle",
    description: "Wildlife enthusiast and conservationist.",
    photo: "/static/images/portrait6.jpg",
    primaryRegions: ["Madhya Pradesh", "Assam"],
    fixedDateDepartures: ["2023-12-01"],
  },
  // Add more agent data objects as needed
];

export default function AgentGallery() {
  const [agents, setAgents] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    // Simulated API call to fetch agents
    const fetchAgents = async () => {
      setIsLoading(true);
      // Replace this with your actual API call
      await new Promise((resolve) => setTimeout(resolve, 1000));
      setAgents(agentData);
      setIsLoading(false);
    };

    fetchAgents();
  }, []);

  const handlePrev = () => {
    setCurrentIndex((prevIndex) => (prevIndex === 0 ? agents.length - 3 : prevIndex - 1));
  };

  const handleNext = () => {
    setCurrentIndex((prevIndex) => (prevIndex === agents.length - 3 ? 0 : prevIndex + 1));
  };

  const displayedAgents = agents.slice(currentIndex, currentIndex + 3);

  return (
    <div className="flex justify-center py-12 bg-white">
      {isLoading ? (
        <div>
          <LoadingPlaceholder />
        </div>
      ) : (
        <div className="flex max-w-6xl space-x-8">
          <div className="flex items-center" style={{ marginTop: "-130px" }}>
            <div className="w-10 h-10 rounded-full bg-[#EBE8E2] flex items-center justify-center">
              <ChevronLeftIcon className="my-auto text-black cursor-pointer" onClick={handlePrev} />
            </div>
          </div>
          <div className="grid grid-cols-3 gap-8">
            {displayedAgents.map((agent) => (
              <div key={agent.id} className="flex flex-col items-center space-y-4">
                <div className="relative">
                  <img
                    alt={agent.name}
                    className="h-[300px] w-[300px] rounded-lg object-cover"
                    height="300"
                    src={agent.photo}
                    style={{ aspectRatio: "300/300", objectFit: "cover" }}
                    width="300"
                  />
                  <div className="absolute inset-0 flex items-center justify-center opacity-0 hover:opacity-100 bg-black bg-opacity-50 transition duration-300">
                    <div className="text-white text-center">
                      <p>Customisable Itineraries</p>
                      {agent.fixedDateDepartures.length > 0 && (
                        <p>
                          Fixed Date Departures: {agent.fixedDateDepartures.join(", ")}
                        </p>
                      )}
                    </div>
                  </div>
                </div>
                <h3 className="text-lg font-semibold">{agent.name}</h3>
                <p className="text-sm text-gray-600">{agent.description}</p>
                <p className="text-sm text-gray-600">
                  Primary Regions: {agent.primaryRegions.join(", ")}
                </p>
                <Button variant="outline">Learn More</Button>
              </div>
            ))}
          </div>
          <div className="flex items-center" style={{ marginTop: "-130px" }}>
            <div className="w-10 h-10 rounded-full bg-[#EBE8E2] flex items-center justify-center">
              <ChevronRightIcon className="my-auto text-black cursor-pointer" onClick={handleNext} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
