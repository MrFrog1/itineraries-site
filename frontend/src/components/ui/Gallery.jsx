import React from 'react';
import { Badge } from "@/components/ui/badge";
import { StarIcon } from './icons';
import { Carousel, CarouselContent, CarouselItem, CarouselNext, CarouselPrevious } from "@/components/ui/carousel";

export default function Gallery({ type, data, horizontal, vertical }) {
  const renderItem = (item, index) => {
    const { name, description, image, price, rating } = item;
    const priceSymbols = Array(price).fill("$").join("");

    return (
      <CarouselItem key={index} className="basis-1/3">
        <div className="flex flex-col items-center space-y-4">
          <div className="relative w-full pb-[75%]">
            <img alt={name} className="absolute inset-0 w-full h-full rounded-lg object-cover" src={image} />
          </div>
          <div className="flex flex-col items-center space-y-2">
            <h3 className="text-lg font-semibold">{name}</h3>
            <p className="text-sm text-gray-600 text-center">{description}</p>
            <div className="flex items-center justify-between w-full">
              <Badge variant="outline">{priceSymbols}</Badge>
              <div className="flex items-center gap-0.5">
                {Array(5)
                  .fill()
                  .map((_, i) => (
                    <StarIcon key={i} className={`h-4 w-4 ${i < rating ? "text-amber-500" : "text-gray-300"}`} />
                  ))}
              </div>
            </div>
          </div>
        </div>
      </CarouselItem>
    );
  };

  return (
    <Carousel>
      <CarouselContent>
        {data.map(renderItem)}
      </CarouselContent>
      <CarouselPrevious className="bg-white text-black">
        <span className="sr-only">Previous</span>
      </CarouselPrevious>
      <CarouselNext className="bg-white text-black">
        <span className="sr-only">Next</span>
      </CarouselNext>
    </Carousel>
  );
}