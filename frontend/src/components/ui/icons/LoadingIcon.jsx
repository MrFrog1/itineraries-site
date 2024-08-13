import React, { useState, useEffect } from 'react';
import { ChevronLeftIcon, ChevronRightIcon, HeartIcon, MountainIcon, CastleIcon, StarIcon, TreesIcon, CloudIcon, CloudRainIcon, CloudSnowIcon, CloudSunIcon, SunIcon, AppleIcon, InstagramIcon, CircleIcon, BirdIcon, TractorIcon } from './index';

const iconComponents = [
  MountainIcon,
  CastleIcon,
  StarIcon,
  TreesIcon,
  CloudSunIcon,
  SunIcon,
  AppleIcon,
  CircleIcon,
  BirdIcon,
  HeartIcon,
  TractorIcon,
];

const LoadingIcon = ({ size = 120 }) => {
  const [currentIconIndex, setCurrentIconIndex] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentIconIndex((prevIndex) => (prevIndex + 1) % iconComponents.length);
    }, 200);

    return () => {
      clearInterval(timer);
    };
  }, []);

  const CurrentIcon = iconComponents[currentIconIndex];

  return (
    <div className="loading-icon">
      <CurrentIcon size={size} />
    </div>
  );
};

export default LoadingIcon;