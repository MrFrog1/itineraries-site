// src/components/admin/AddComponent.jsx

import React, { useState } from "react";
import { useDispatch } from 'react-redux';
import { useAddComponentMutation } from '../../services/api';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select";
import { Button } from "@/components/ui/button";

export default function AddComponent() {
  const [showPricing, setShowPricing] = useState(false);
  const [showCommissionedRates, setShowCommissionedRates] = useState(false);
  const [addComponent] = useAddComponentMutation();
  const dispatch = useDispatch();

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    const componentData = Object.fromEntries(formData.entries());
    
    try {
      await addComponent(componentData).unwrap();
      // Handle success
    } catch (error) {
      // Handle error
    }
  };

  return (
    <Card className="w-full max-w-4xl">
      <CardHeader>
        <CardTitle>Create New Component</CardTitle>
        <CardDescription>Fill out the details to create a new component.</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="grid gap-4">
          {/* Form fields as per the v0.dev code */}
          {/* ... */}
        </form>
      </CardContent>
      <CardFooter>
        <Button type="submit">Create Component</Button>
      </CardFooter>
    </Card>
  );
}