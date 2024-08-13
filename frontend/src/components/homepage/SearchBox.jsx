import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select";
import { Popover, PopoverTrigger, PopoverContent } from "@/components/ui/popover";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { CarIcon, LocateIcon, HotelIcon, SpadeIcon, MountainIcon, HomeIcon } from '../ui/icons';
import { setSearchParams } from '../../features/search/searchSlice';
import ChatBox from './ChatBox.jsx';

const SearchBox = () => {
  const dispatch = useDispatch();
  const { searchParams, regions } = useSelector(state => state.search);
  const [showLocationDropdown, setShowLocationDropdown] = useState(false);
  const [isLocationEnabled, setIsLocationEnabled] = useState(false);

  const handleSearchParamChange = (paramName, value) => {
    dispatch(setSearchParams({ [paramName]: value }));
  };

  const handleLocationSelect = (value) => {
    const currentLocations = searchParams.location ? searchParams.location.split(',') : [];
    const newLocations = currentLocations.includes(value)
      ? currentLocations.filter(loc => loc !== value)
      : [...currentLocations, value];
    handleSearchParamChange('location', newLocations.join(','));
  };


  const handleTypeChange = (value) => {
    const currentTypes = searchParams.type ? searchParams.type.split(',') : [];
    const newTypes = currentTypes.includes(value)
      ? currentTypes.filter(type => type !== value)
      : [...currentTypes, value];
    handleSearchParamChange('type', newTypes.join(','));
  };

  const handleButtonClick = (button) => {
    const newSelectedButtons = searchParams.selectedButtons.includes(button)
      ? searchParams.selectedButtons.filter(b => b !== button)
      : [...searchParams.selectedButtons, button];
    handleSearchParamChange('selectedButtons', newSelectedButtons);
  };

  const toggleLocationEnabled = () => {
    setIsLocationEnabled(!isLocationEnabled);
    // Here you would typically trigger geolocation and update the search params
  };
  return (
    <div className="w-full max-w-md mx-auto p-4">
      <div className="bg-white border border-gray-200 rounded-lg p-4">
        <Tabs value={searchParams.activeTab} onValueChange={(value) => handleSearchParamChange('activeTab', value)} className="border-b border-gray-200 mb-4">
          <TabsList className="flex justify-between">
            <TabsTrigger value="hotels" className="flex-1 text-center">Hotels</TabsTrigger>
            <TabsTrigger value="itineraries" className="flex-1 text-center">Itineraries</TabsTrigger>
          </TabsList>
        </Tabs>
        <div className="space-y-4">
          <div className="relative">
            <Input
              type="text"
              placeholder="Select locations..."
              className="w-full"
              value={searchParams.location}
              onChange={(e) => handleSearchParamChange('location', e.target.value)}
              onFocus={() => setShowLocationDropdown(true)}
              onBlur={() => setTimeout(() => setShowLocationDropdown(false), 200)}
            />
            {showLocationDropdown && (
              <div className="absolute z-10 w-full bg-white border border-gray-300 mt-1 rounded-md shadow-lg max-h-60 overflow-auto">
                {regions.map((region) => (
                  <div
                    key={region.id}
                    className="p-2 hover:bg-gray-100 cursor-pointer"
                    onMouseDown={() => handleLocationSelect(region.name)}
                  >
                    <input
                      type="checkbox"
                      checked={searchParams.location && searchParams.location.includes(region.name)}
                      readOnly
                      className="mr-2"
                    />
                    {region.name}
                  </div>
                ))}
              </div>
            )}
          </div>
          <Popover>
            <PopoverTrigger asChild>
              <Button variant="outline" className="w-full justify-start">
                {searchParams.type ? searchParams.type.split(',').join(', ') : 'Select types...'}
              </Button>
            </PopoverTrigger>
            <PopoverContent className="w-full p-0">
              <div className="p-2">
                {searchParams.activeTab === 'hotels' ? (
                  <>
                    {['Luxury', 'Budget', 'Family', 'Romantic'].map((type) => (
                      <div key={type} className="flex items-center p-2">
                        <input
                          type="checkbox"
                          id={type}
                          checked={searchParams.type && searchParams.type.includes(type.toLowerCase())}
                          onChange={() => handleTypeChange(type.toLowerCase())}
                          className="mr-2"
                        />
                        <label htmlFor={type}>{type}</label>
                      </div>
                    ))}
                  </>
                ) : (
                  <>
                    {['Hiking', 'Wildlife', 'Cultural', 'Adventure'].map((type) => (
                      <div key={type} className="flex items-center p-2">
                        <input
                          type="checkbox"
                          id={type}
                          checked={searchParams.type && searchParams.type.includes(type.toLowerCase())}
                          onChange={() => handleTypeChange(type.toLowerCase())}
                          className="mr-2"
                        />
                        <label htmlFor={type}>{type}</label>
                      </div>
                    ))}
                  </>
                )}
              </div>
            </PopoverContent>
          </Popover>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Min Price</label>
              <select
                className="w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
                value={searchParams.minPrice}
                onChange={(e) => handleSearchParamChange('minPrice', e.target.value)}
              >
                {[...Array(50)].map((_, i) => (
                  <option key={i} value={(i + 1) * 1000}>
                    {((i + 1) * 1000).toLocaleString()}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Max Price</label>
              <select
                className="w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
                value={searchParams.maxPrice}
                onChange={(e) => handleSearchParamChange('maxPrice', e.target.value)}
              >
                {[...Array(49)].map((_, i) => (
                  <option key={i} value={(i + 2) * 1000}>
                    {((i + 2) * 1000).toLocaleString()}
                  </option>
                ))}
                <option value="50000+">50,000+</option>
              </select>
            </div>
          </div>
          <div className="relative">
            <Input
              type="number"
              placeholder="How many hours from your location?"
              className="w-full pr-12"
              value={searchParams.hoursFrom}
              onChange={(e) => handleSearchParamChange('hoursFrom', e.target.value)}
            />
            <div className="absolute inset-y-0 right-0 flex items-center pr-3">
              <Select onValueChange={(value) => handleSearchParamChange('hoursMode', value)}>
                <SelectTrigger className="w-24">
                  <SelectValue placeholder="Mode">
                    {searchParams.hoursMode === 'driving' ? <CarIcon className="h-4 w-4" /> : 'Flying'}
                  </SelectValue>
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="driving">Driving</SelectItem>
                  <SelectItem value="flying">Flying</SelectItem>
                </SelectContent>
              </Select>
              <Button
                variant="ghost"
                size="icon"
                className={`rounded-full ml-2 ${isLocationEnabled ? 'bg-gray-200' : ''}`}
                onClick={toggleLocationEnabled}
              >
                <LocateIcon className="h-4 w-4 text-gray-500" />
              </Button>
            </div>
          </div>
          <ChatBox/>
        </div>
      </div>
      <div className="grid grid-cols-2 gap-4 mt-4 px-4">
        {searchParams.activeTab === "hotels" ? (
          <>
            <Button
              variant={searchParams.selectedButtons.includes("highly-personal") ? "default" : "outline"}
              onClick={() => handleButtonClick("highly-personal")}
              className="flex items-center space-x-2 w-full"
            >
              <HotelIcon className="h-4 w-4" />
              <span className="text-sm">Highly Personal</span>
            </Button>
            <Button
              variant={searchParams.selectedButtons.includes("pampering") ? "default" : "outline"}
              onClick={() => handleButtonClick("pampering")}
              className="flex items-center space-x-2 w-full"
            >
              <SpadeIcon className="h-4 w-4" />
              <span className="text-sm">Pampering</span>
            </Button>
            <Button
              variant={searchParams.selectedButtons.includes("spectacular-views") ? "default" : "outline"}
              onClick={() => handleButtonClick("spectacular-views")}
              className="flex items-center space-x-2 w-full"
            >
              <MountainIcon className="h-4 w-4" />
              <span className="text-sm">Spectacular Views</span>
            </Button>
            <Button
              variant={searchParams.selectedButtons.includes("unorthodox") ? "default" : "outline"}
              onClick={() => handleButtonClick("unorthodox")}
              className="flex items-center space-x-2 w-full"
            >
              <HomeIcon className="h-4 w-4" />
              <span className="text-sm">Unorthodox</span>
            </Button>
          </>
        ) : (
          <>
            <Button
              variant={searchParams.selectedButtons.includes("once-in-a-lifetime") ? "default" : "outline"}
              onClick={() => handleButtonClick("once-in-a-lifetime")}
              className="flex items-center space-x-2 w-full"
            >
              <MountainIcon className="h-4 w-4" />
              <span className="text-sm">Once-in-a-lifetime</span>
            </Button>
            <Button
              variant={searchParams.selectedButtons.includes("jam-packed") ? "default" : "outline"}
              onClick={() => handleButtonClick("jam-packed")}
              className="flex items-center space-x-2 w-full"
            >
              <span className="text-sm">Jam-packed</span>
            </Button>
            <Button
              variant={searchParams.selectedButtons.includes("pampering") ? "default" : "outline"}
              onClick={() => handleButtonClick("pampering")}
              className="flex items-center space-x-2 w-full"
            >
              <SpadeIcon className="h-4 w-4" />
              <span className="text-sm">Pampering</span>
            </Button>
            <Button
              variant={searchParams.selectedButtons.includes("fascinating") ? "default" : "outline"}
              onClick={() => handleButtonClick("fascinating")}
              className="flex items-center space-x-2 w-full"
            >
              <HomeIcon className="h-4 w-4" />
              <span className="text-sm">Fascinating</span>
            </Button>
          </>
        )}
      </div>
      <div className="w-full pt-4 mt-4 px-4">
        <h3 className="text-lg font-bold text-center mb-4">Unsure of Where to Go? Search by Region</h3>
        <div className="flex flex-col gap-4">
          <div>
            <h3 className="text-sm font-medium text-muted-foreground italic mb-2 text-center">Best in...</h3>
            <Select 
              value={searchParams.month} 
              onValueChange={(value) => handleSearchParamChange('month', value)} 
              className="w-full"
            >
              <SelectTrigger>
                <SelectValue placeholder="Select month" />
              </SelectTrigger>
              <SelectContent>
                {["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"].map((month) => (
                  <SelectItem key={month.toLowerCase()} value={month.toLowerCase()}>{month}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div>
            <h3 className="text-sm font-medium text-muted-foreground italic mb-2 text-center">Best for...</h3>
            <Select 
              value={searchParams.bestFor} 
              onValueChange={(value) => handleSearchParamChange('bestFor', value)} 
              className="w-full"
            >
              <SelectTrigger>
                <SelectValue placeholder="Select category" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="culture">Culture</SelectItem>
                <SelectItem value="cuisine">Cuisine</SelectItem>
                <SelectItem value="adventure">Adventure</SelectItem>
                <SelectItem value="landscapes">Landscapes</SelectItem>
                <SelectItem value="textiles">Textiles</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SearchBox;