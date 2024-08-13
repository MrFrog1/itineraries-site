import React, { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import InfiniteScroll from 'react-infinite-scroll-component';
import { motion, AnimatePresence } from 'framer-motion';
import { Carousel, CarouselContent, CarouselItem, CarouselPrevious, CarouselNext } from "@/components/ui/carousel";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { ChevronLeftIcon, ChevronRightIcon } from '../ui/icons';
import { useGetHotelsQuery, useGetItinerariesQuery, useGetRegionsQuery, useGetDetailedRegionsMutation, useChatMutation } from '../../services/api';
import { selectFilteredResults } from '../../features/search/searchSlice';
import LazyImage from '../ui/LazyImage';

const Gallery = () => {
  const { searchParams } = useSelector(state => state.search);
  const filteredResults = useSelector(selectFilteredResults);
  
  const { data: hotels, isLoading: isLoadingHotels } = useGetHotelsQuery();
  const { data: itineraries, isLoading: isLoadingItineraries } = useGetItinerariesQuery();
  const { data: regions, isLoading: isLoadingRegions } = useGetRegionsQuery();
  const [getDetailedRegions, { data: detailedRegions }] = useGetDetailedRegionsMutation();

  const [items, setItems] = useState([]);
  const [hasMore, setHasMore] = useState(true);
  const [page, setPage] = useState(1);
  const itemsPerPage = 5;

  const [showChat, setShowChat] = useState(false);
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [chat, { isLoading: isChatLoading }] = useChatMutation();

  useEffect(() => {
    if (filteredResults[searchParams.activeTab]) {
      setItems(filteredResults[searchParams.activeTab].slice(0, itemsPerPage));
      setHasMore(filteredResults[searchParams.activeTab].length > itemsPerPage);
      setPage(1);
    } else {
      setItems([]);
      setHasMore(false);
    }
  }, [filteredResults, searchParams.activeTab]);

  const fetchMoreData = () => {
    const nextItems = filteredResults[searchParams.activeTab].slice(
      page * itemsPerPage,
      (page + 1) * itemsPerPage
    );
    
    if (nextItems.length > 0) {
      setItems(prevItems => [...prevItems, ...nextItems]);
      setPage(prevPage => prevPage + 1);
    } else {
      setHasMore(false);
    }
  };

  const handleChatSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');

    try {
      const response = await chat({ message: input }).unwrap();
      setMessages(prev => [...prev, { role: 'assistant', content: response.message, citation: response.citation }]);
    } catch (error) {
      console.error('Failed to send message:', error);
      setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, I encountered an error. Please try again.' }]);
    }
  };

  if (isLoadingHotels || isLoadingItineraries || isLoadingRegions) {
    return <div>Loading...</div>;
  }

  const renderImageCarousel = (images) => (
    <Carousel className="rounded-lg overflow-hidden">
      <CarouselContent>
        {images && images.map((image, imageIndex) => (
          <CarouselItem key={imageIndex}>
            <LazyImage
              src={image.image}
              alt={`Image ${imageIndex + 1}`}
              className="object-cover w-full h-64"
            />
          </CarouselItem>
        ))}
      </CarouselContent>
      <CarouselPrevious className="absolute top-1/2 -translate-y-1/2 left-4 z-10 text-white hover:text-primary transition-colors">
        <ChevronLeftIcon className="w-6 h-6" />
      </CarouselPrevious>
      <CarouselNext className="absolute top-1/2 -translate-y-1/2 right-4 z-10 text-white hover:text-primary transition-colors">
        <ChevronRightIcon className="w-6 h-6" />
      </CarouselNext>
    </Carousel>
  );

  const renderInfoCarousel = (item) => (
    <Carousel className="rounded-lg overflow-hidden">
      <CarouselContent>
        {[1, 2, 3].map((_, index) => (
          <CarouselItem key={index}>
            <div className="relative h-64 bg-gradient-to-r from-blue-500 to-purple-500">
              <div className="absolute inset-0 flex flex-col justify-center items-center text-white p-4">
                <h3 className="text-2xl font-bold mb-2">{item.name}</h3>
                {searchParams.activeTab === 'hotels' ? (
                  <>
                    <p className="text-lg mb-1">Type: {item.type}</p>
                    <p className="text-lg mb-1">Price: ${item.min_price_in_INR}</p>
                    <p className="text-sm">{item.short_visible_description}</p>
                  </>
                ) : (
                  <>
                    <p className="text-lg mb-1">Type: {item.type}</p>
                    <p className="text-lg mb-1">Price: ${item.cost_for_1_pax}</p>
                    <p className="text-sm">{item.short_visible_description}</p>
                  </>
                )}
              </div>
            </div>
          </CarouselItem>
        ))}
      </CarouselContent>
      <CarouselPrevious className="absolute top-1/2 -translate-y-1/2 left-4 z-10 text-white hover:text-primary transition-colors">
        <ChevronLeftIcon className="w-6 h-6" />
      </CarouselPrevious>
      <CarouselNext className="absolute top-1/2 -translate-y-1/2 right-4 z-10 text-white hover:text-primary transition-colors">
        <ChevronRightIcon className="w-6 h-6" />
      </CarouselNext>
    </Carousel>
  );

  const renderItem = (item) => (
    <div key={item.id} className="grid grid-cols-2 gap-6 mb-8">
      <div className="col-span-1">
        {renderImageCarousel(item.images)}
      </div>
      <div className="col-span-1">
        {renderInfoCarousel(item)}
      </div>
    </div>
  );


  return (
    <div className="max-w-6xl mx-auto py-12 px-4 md:px-6">
      <Button onClick={() => setShowChat(!showChat)} className="mb-4">
        {showChat ? `Return to ${searchParams.activeTab}` : 'Show Chat Response'}
      </Button>
      <AnimatePresence mode="wait">
        {showChat && chatResponse ? (
          <motion.div
            key="chat"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
            className="border rounded-lg p-4 mb-4"
          >
            <p className="font-bold">You asked:</p>
            <p className="mb-2">{chatResponse.userMessage}</p>
            <p className="font-bold">Assistant's response:</p>
            <p>{chatResponse.assistantMessage}</p>
            {chatResponse.citation && (
              <p className="text-sm text-gray-500 mt-2">Source: {chatResponse.citation}</p>
            )}
          </motion.div>
        ) : (
          <motion.div
            key="gallery"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            {items.length > 0 ? (
              <InfiniteScroll
                dataLength={items.length}
                next={fetchMoreData}
                hasMore={hasMore}
                loader={<h4>Loading...</h4>}
                endMessage={
                  <p style={{ textAlign: 'center' }}>
                    <b>You have seen it all</b>
                  </p>
                }
              >
                {items.map(renderItem)}
              </InfiniteScroll>
            ) : (
              <div className="text-center">
                <p>No results found for the current filters.</p>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default Gallery;