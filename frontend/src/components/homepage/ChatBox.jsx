import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useChatMutation } from '../../services/api';
import { setSearchParams } from '../../features/search/searchSlice';

const ChatBox = () => {
  const [input, setInput] = useState('');
  const dispatch = useDispatch();
  const [chat, { isLoading }] = useChatMutation();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    try {
      const response = await chat({ message: input }).unwrap();
      dispatch(setSearchParams({ chatResponse: { 
        userMessage: input, 
        assistantMessage: response.message, 
        citation: response.citation 
      }}));
      setInput('');
    } catch (error) {
      console.error('Failed to send message:', error);
      dispatch(setSearchParams({ chatResponse: { 
        userMessage: input, 
        assistantMessage: 'Sorry, I encountered an error. Please try again.', 
        citation: null 
      }}));
    }
  };

  return (
    <div className="flex flex-col border rounded-lg p-4">
      <form onSubmit={handleSubmit} className="flex">
        <Textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Making travel personal.... with a chatbot! Ask me anything! About an itinerary, a region, the weather or the meaning of life"
          className="flex-1 mr-2"
        />
        <Button type="submit" disabled={isLoading}>Send</Button>
      </form>
    </div>
  );
};

export default ChatBox;