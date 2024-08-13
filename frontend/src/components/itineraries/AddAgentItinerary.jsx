// src/components/admin/AddAgentItinerary.jsx

import React from 'react';
import { useDispatch } from 'react-redux';
import { useAddAgentItineraryMutation } from '../../services/api';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";

export default function AddAgentItinerary() {
  const [addAgentItinerary] = useAddAgentItineraryMutation();
  const dispatch = useDispatch();

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    const itineraryData = Object.fromEntries(formData.entries());
    
    try {
      await addAgentItinerary(itineraryData).unwrap();
      // Handle success
    } catch (error) {
      // Handle error
    }
  };

  return (
    <Card className="w-full max-w-4xl">
      <CardHeader>
        <CardTitle>Add Agent Itinerary</CardTitle>
        <CardDescription>Create a new itinerary for an agent.</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="grid gap-4">
          <div>
            <Label htmlFor="name">Itinerary Name</Label>
            <Input id="name" name="name" required />
          </div>
          <div>
            <Label htmlFor="description">Description</Label>
            <Textarea id="description" name="description" required />
          </div>
          {/* Add more fields as needed */}
        </form>
      </CardContent>
      <CardFooter>
        <Button type="submit">Create Itinerary</Button>
      </CardFooter>
    </Card>
  );
}