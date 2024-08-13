
import React, { useState } from 'react';
import { Card, CardHeader, CardContent } from '@/components/ui/card';
import { SunIcon, CloudIcon, CloudRainIcon, CloudSnowIcon, CloudSunIcon } from '../ui/icons';
import { Button } from '@/components/ui/button';


const IndiaMapInfoBox = ({ infoBox, regionMapping, selectedLabel, onViewHotelsOrItineraries, weatherMode, monthlyData, onClose }) => {
  const [showDescription, setShowDescription] = useState(false);
  const [showMonthlyData, setShowMonthlyData] = useState(false);

  const handleViewInfo = () => {
    setShowDescription(!showDescription);
  };

  const handleToggleMonthlyData = () => {
    setShowMonthlyData(!showMonthlyData);
  };

  if (weatherMode) {
    if (monthlyData.length === 0) {
      return (
        <Card className="w-full max-w-xs mx-auto">
          <div className="p-4 grid gap-4">
            <CardHeader className="p-0">
              <div className="flex items-center gap-4">
                <h2 className="text-lg font-bold">{regionMapping[infoBox]?.name || infoBox}</h2>
              </div>
            </CardHeader>
            <CardContent className="p-0">
              <div className="text-sm font-medium text-gray-500">
                <p className="text-sm font-medium text-gray-500">No weather information available for this region.</p>
              </div>
            </CardContent>
          </div>
        </Card>
      );
    }

    return (
      <Card className="w-full max-w-xs mx-auto">
        <div className="p-4 grid gap-4">
          <CardHeader className="p-0">
            <div className="flex items-center gap-4">
              {monthlyData[0].icon && (
                <>
                  {monthlyData[0].icon === 'SunIcon' && <SunIcon className="h-6 w-6" />}
                  {monthlyData[0].icon === 'CloudIcon' && <CloudIcon className="h-6 w-6" />}
                  {monthlyData[0].icon === 'CloudRainIcon' && <CloudRainIcon className="h-6 w-6" />}
                  {monthlyData[0].icon === 'CloudSnowIcon' && <CloudSnowIcon className="h-6 w-6" />}
                  {monthlyData[0].icon === 'CloudSunIcon' && <CloudSunIcon className="h-6 w-6" />}
                </>
              )}
              <h2 className="text-lg font-bold">{regionMapping[infoBox]?.name || infoBox}</h2>
            </div>
          </CardHeader>
          <CardContent className="p-0">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="text-2xl font-semibold">{monthlyData[0].temperature}°</div>
              </div>
              <div className="text-sm font-medium text-gray-500">
                <p className="text-sm font-medium text-gray-500">{monthlyData[0].icon ? monthlyData[0].icon.replace('Icon', '') : 'N/A'}</p>
              </div>
            </div>
            <button className="mt-4 text-blue-500" onClick={handleToggleMonthlyData}>
              {showMonthlyData ? '-' : '+ Show Monthly Weather'}
            </button>
            {showMonthlyData && (
              <div>
                {monthlyData.map((data, index) => (
                  <div key={index} className="mt-4">
                    <table className="w-full">
                      <thead>
                        <tr>
                          <th className="px-4 py-2">Month</th>
                          <th className="px-4 py-2">Temp. Range</th>
                          <th className="px-4 py-2">Weather</th>
                          <th className="px-4 py-2">Seasonal Rating</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr>
                          <td className="px-4 py-2">{data.month}</td>
                          <td className="px-4 py-2">{data.temperature || 'N/A'}°</td>
                          <td className="px-4 py-2">
                            {data.icon ? (
                              <>
                                {data.icon === 'SunIcon' && <SunIcon className="h-6 w-6" />}
                                {data.icon === 'CloudIcon' && <CloudIcon className="h-6 w-6" />}
                                {data.icon === 'CloudRainIcon' && <CloudRainIcon className="h-6 w-6" />}
                                {data.icon === 'CloudSnowIcon' && <CloudSnowIcon className="h-6 w-6" />}
                                {data.icon === 'CloudSunIcon' && <CloudSunIcon className="h-6 w-6" />}
                              </>
                            ) : (
                              'N/A'
                            )}
                          </td>
                          <td className="px-4 py-2">{data.rating || 'N/A'}</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </div>
      </Card>
    );
  }

  return (
    <div className="w-full max-w-sm p-6 bg-white rounded-xl border">
      <h1 className="text-2xl font-bold">
        {regionMapping[infoBox]?.name || infoBox}{' '}
        <Button variant="ghost" onClick={handleViewInfo}>
          {showDescription ? 'Hide Info -' : 'View Info +'}
        </Button>
      </h1>
      <div className="flex flex-col gap-4 mt-4">
        <Button className="flex-1 w-1/2" variant="outline" onClick={onViewHotelsOrItineraries}>
          {selectedLabel === 'All' && 'View Hotels & Itineraries'}
          {selectedLabel === 'Hotels' && 'View Hotels'}
          {selectedLabel === 'Itineraries' && 'View Itineraries'}
        </Button>
        {showDescription && (
          <p className="text-sm text-gray-700 dark:text-gray-300">{regionMapping[infoBox]?.description}</p>
        )}
      </div>
    </div>
  );
};

export default IndiaMapInfoBox;