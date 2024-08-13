import React, { useState } from 'react';
import { useAddAgentMutation } from '../../services/api';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { Switch } from "@/components/ui/switch";
import { Button } from "@/components/ui/button";
import { useToast } from "@/components/ui/use-toast";

export default function AddAgent() {
  const [addAgent, { isLoading }] = useAddAgentMutation();
  const { toast } = useToast();
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    email: '',
    phone_number: '',
    country: '',
    nickname: '',
    region: '',
    is_agent: true,
    short_bio: '',
    bio: '',
    business_name: '',
    website: '',
    instagram_link: '',
    sustainability_practices: '',
    hotel_owner: false,
    default_commission_percentage: '',
    default_organisation_fee: '',
  });
  const [errors, setErrors] = useState({});

  const validateForm = () => {
    let newErrors = {};
    if (!formData.username) newErrors.username = "Username is required";
    if (!formData.password) newErrors.password = "Password is required";
    if (!formData.email) newErrors.email = "Email is required";
    if (formData.email && !/^\S+@\S+\.\S+$/.test(formData.email)) newErrors.email = "Invalid email format";
    if (!formData.phone_number) newErrors.phone_number = "Phone number is required";
    if (!formData.country) newErrors.country = "Country is required";
    if (!formData.region) newErrors.region = "Region is required";
    if (formData.default_commission_percentage && (isNaN(formData.default_commission_percentage) || formData.default_commission_percentage < 0 || formData.default_commission_percentage > 100)) {
      newErrors.default_commission_percentage = "Commission percentage must be between 0 and 100";
    }
    if (formData.default_organisation_fee && (isNaN(formData.default_organisation_fee) || formData.default_organisation_fee < 0)) {
      newErrors.default_organisation_fee = "Organisation fee must be a non-negative number";
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSelectChange = (name, value) => {
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!validateForm()) {
      toast({
        title: "Validation Error",
        description: "Please correct the errors in the form.",
        status: "error"
      });
      return;
    }
    try {
      await addAgent(formData).unwrap();
      toast({
        title: "Agent Added",
        description: "The agent has been successfully added.",
        status: "success"
      });
      // Reset form or redirect
    } catch (error) {
      toast({
        title: "Error",
        description: error.data?.detail || "Failed to add agent. Please try again.",
        status: "error"
      });
    }
  };

  return (
    <Card className="w-full max-w-4xl">
      <CardHeader>
        <CardTitle>Add an Agent</CardTitle>
        <CardDescription>Fill out the details to create a new agent account.</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="grid gap-6">
          <div className="grid grid-cols-2 gap-6">
            <div className="grid gap-2">
              <Label htmlFor="username">Username</Label>
              <Input id="username" name="username" value={formData.username} onChange={handleInputChange} required />
              {errors.username && <p className="text-red-500">{errors.username}</p>}
            </div>
            <div className="grid gap-2">
              <Label htmlFor="password">Password</Label>
              <Input id="password" name="password" type="password" value={formData.password} onChange={handleInputChange} required />
              {errors.password && <p className="text-red-500">{errors.password}</p>}
            </div>
          </div>
          <div className="grid grid-cols-2 gap-6">
            <div className="grid gap-2">
              <Label htmlFor="email">Email</Label>
              <Input id="email" name="email" type="email" value={formData.email} onChange={handleInputChange} required />
              {errors.email && <p className="text-red-500">{errors.email}</p>}
            </div>
            <div className="grid gap-2">
              <Label htmlFor="phone_number">Phone Number</Label>
              <Input id="phone_number" name="phone_number" value={formData.phone_number} onChange={handleInputChange} required />
              {errors.phone_number && <p className="text-red-500">{errors.phone_number}</p>}
            </div>
          </div>
          <div className="grid grid-cols-2 gap-6">
            <div className="grid gap-2">
              <Label htmlFor="country">Country</Label>
              <Input id="country" name="country" value={formData.country} onChange={handleInputChange} required />
              {errors.country && <p className="text-red-500">{errors.country}</p>}
            </div>
            <div className="grid gap-2">
              <Label htmlFor="region">Region</Label>
              <Input id="region" name="region" value={formData.region} onChange={handleInputChange} required />
              {errors.region && <p className="text-red-500">{errors.region}</p>}
            </div>
          </div>
          <div className="grid gap-2">
            <Label htmlFor="short_bio">Short Bio</Label>
            <Textarea id="short_bio" name="short_bio" value={formData.short_bio} onChange={handleInputChange} />
          </div>
          <div className="grid gap-2">
            <Label htmlFor="bio">Full Bio</Label>
            <Textarea id="bio" name="bio" value={formData.bio} onChange={handleInputChange} />
          </div>
          <div className="grid grid-cols-2 gap-6">
            <div className="grid gap-2">
              <Label htmlFor="business_name">Business Name</Label>
              <Input id="business_name" name="business_name" value={formData.business_name} onChange={handleInputChange} />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="website">Website</Label>
              <Input id="website" name="website" type="url" value={formData.website} onChange={handleInputChange} />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-6">
            <div className="grid gap-2">
              <Label htmlFor="instagram_link">Instagram Link</Label>
              <Input id="instagram_link" name="instagram_link" type="url" value={formData.instagram_link} onChange={handleInputChange} />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="sustainability_practices">Sustainability Practices</Label>
              <Textarea id="sustainability_practices" name="sustainability_practices" value={formData.sustainability_practices} onChange={handleInputChange} />
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Switch id="hotel_owner" name="hotel_owner" checked={formData.hotel_owner} onCheckedChange={(checked) => handleSelectChange('hotel_owner', checked)} />
            <Label htmlFor="hotel_owner">Hotel Owner</Label>
          </div>
          <div className="grid grid-cols-2 gap-6">
            <div className="grid gap-2">
              <Label htmlFor="default_commission_percentage">Default Commission Percentage</Label>
              <Input id="default_commission_percentage" name="default_commission_percentage" type="number" value={formData.default_commission_percentage} onChange={handleInputChange} />
              {errors.default_commission_percentage && <p className="text-red-500">{errors.default_commission_percentage}</p>}
            </div>
            <div className="grid gap-2">
              <Label htmlFor="default_organisation_fee">Default Organisation Fee</Label>
              <Input id="default_organisation_fee" name="default_organisation_fee" type="number" value={formData.default_organisation_fee} onChange={handleInputChange} />
              {errors.default_organisation_fee && <p className="text-red-500">{errors.default_organisation_fee}</p>}
            </div>
          </div>
        </form>
      </CardContent>
      <CardFooter>
        <Button type="submit" disabled={isLoading} onClick={handleSubmit}>
          {isLoading ? 'Adding Agent...' : 'Add Agent'}
        </Button>
      </CardFooter>
    </Card>
  );
}