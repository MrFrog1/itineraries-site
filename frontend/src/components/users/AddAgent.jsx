import React, { useState, useCallback } from 'react';
import { useAddAgentMutation, useAddPotentialAgentMutation, useGetAllAgentsQuery } from '../../services/api';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { Switch } from "@/components/ui/switch";
import { Button } from "@/components/ui/button";
import { useToast } from "@/components/ui/use-toast";
import SearchInput from '../ui/SearchInput';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  MultiSelector,
  MultiSelectorTrigger,
  MultiSelectorInput,
  MultiSelectorContent,
  MultiSelectorList,
  MultiSelectorItem,
} from "@/components/ui/multiselector";

const expertiseCategoryOptions = [
  { value: 'adventure', label: 'Adventure' },
  { value: 'cultural', label: 'Cultural' },
  { value: 'luxury', label: 'Luxury' },
];

export default function AddAgent() {
  const [addAgent, { isLoading: isAddingAgent }] = useAddAgentMutation();
  const [addPotentialAgent, { isLoading: isAddingPotentialAgent }] = useAddPotentialAgentMutation();
  const { data: allAgents, isLoading: isLoadingAgents } = useGetAllAgentsQuery();
  const [selectedAgentId, setSelectedAgentId] = useState(null);
  const { toast } = useToast();
  const [agentType, setAgentType] = useState('user');
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    first_name: '',
    last_name: '',
    email: '',
    phone_number: '',
    country: '',
    nickname: '',
    region: '',
    expertise_categories: [],
    is_agent: true,
    short_bio: '',
    bio: '',
    business_name: '',
    website: '',
    instagram_link: '',
    sustainability_practices: '',
    hotel_owner: false,
    public_profile: false,
    default_commission_percentage: '',
    default_organisation_fee: '',
    accompanying_agent: '',
    admin_description: '',
  });
  const [errors, setErrors] = useState({});

  const validateForm = () => {
    let newErrors = {};
    if (agentType === 'user') {
      if (!formData.username) newErrors.username = "Username is required";
      if (!formData.password) newErrors.password = "Password is required";
    }
    if (!formData.first_name) newErrors.first_name = "First name is required";
    if (!formData.last_name) newErrors.last_name = "Last name is required";
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

  const handleInputChange = useCallback((e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  }, []);

  const handleSelectChange = useCallback((name, value) => {
    setFormData(prev => ({ ...prev, [name]: value }));
  }, []);


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

  // Create a copy of the form data
  const submissionData = { ...formData };

  // Remove fields that are not needed for PotentialAgent if that's the current type
  if (agentType === 'potential') {
    const potentialAgentFields = [
      'first_name', 'last_name', 'email_address', 'phone_number', 'country',
      'region', 'short_bio', 'bio', 'business_name', 'website', 'instagram_link',
      'expertise_categories', 'hotel_owner', 'admin_description'
    ];
    Object.keys(submissionData).forEach((key) => {
      if (!potentialAgentFields.includes(key)) {
        delete submissionData[key];
      }
    });
  }
  console.log(submissionData);

  try {
    let response;
    if (agentType === 'user') {
      response = await addAgent(submissionData).unwrap();
    } else {
      response = await addPotentialAgent(submissionData).unwrap();
    }
    toast({
      title: `${agentType === 'user' ? 'Agent' : 'Potential Agent'} Added`,
      description: `The ${agentType === 'user' ? 'agent' : 'potential agent'} has been successfully added.`,
      status: "success"
    });
    // Reset form or redirect
  } catch (error) {
    console.error('Failed to add agent:', error);
    let errorMessage = `Failed to add ${agentType === 'user' ? 'agent' : 'potential agent'}. Please try again.`;
    if (error.data) {
      if (typeof error.data === 'string') {
        errorMessage = error.data;
      } else if (typeof error.data === 'object') {
        errorMessage = Object.entries(error.data)
          .map(([key, value]) => `${key}: ${value}`)
          .join('\n');
      }
    }
    toast({
      title: "Error",
      description: errorMessage,
      status: "error"
    });
  }
};

  const handleAgentSelect = (agent) => {
    console.log("Selected agent:", agent);
    setFormData(prev => ({ ...prev, accompanying_agent: agent.id }));
    setSelectedAgentId(agent.id);
  };

const renderForm = () => (
  <form onSubmit={handleSubmit} className="space-y-4">
    {agentType === 'user' && (
      <>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <Label htmlFor="username">Username</Label>
            <Input id="username" name="username" value={formData.username} onChange={handleInputChange} required />
            {errors.username && <p className="text-red-500">{errors.username}</p>}
          </div>
          <div>
            <Label htmlFor="password">Password</Label>
            <Input id="password" name="password" type="password" value={formData.password} onChange={handleInputChange} required />
            {errors.password && <p className="text-red-500">{errors.password}</p>}
          </div>
        </div>
      </>
    )}
    
    <div className="grid grid-cols-2 gap-4">
      <div>
        <Label htmlFor="first_name">First Name</Label>
        <Input id="first_name" name="first_name" value={formData.first_name} onChange={handleInputChange} required />
        {errors.first_name && <p className="text-red-500">{errors.first_name}</p>}
      </div>
      <div>
        <Label htmlFor="last_name">Last Name</Label>
        <Input id="last_name" name="last_name" value={formData.last_name} onChange={handleInputChange} required />
        {errors.last_name && <p className="text-red-500">{errors.last_name}</p>}
      </div>
    </div>

    <div className="grid grid-cols-2 gap-4">
      <div>
        <Label htmlFor="email">Email</Label>
        <Input id="email" name="email" type="email" value={formData.email} onChange={handleInputChange} required />
        {errors.email && <p className="text-red-500">{errors.email}</p>}
      </div>
      <div>
        <Label htmlFor="phone_number">Phone Number</Label>
        <Input id="phone_number" name="phone_number" value={formData.phone_number} onChange={handleInputChange} required />
        {errors.phone_number && <p className="text-red-500">{errors.phone_number}</p>}
      </div>
    </div>

    <div className="grid grid-cols-2 gap-4">
      <div>
        <Label htmlFor="country">Country</Label>
        <Input id="country" name="country" value={formData.country} onChange={handleInputChange} required />
        {errors.country && <p className="text-red-500">{errors.country}</p>}
      </div>
      <div>
        <Label htmlFor="region">Region</Label>
        <Input id="region" name="region" value={formData.region} onChange={handleInputChange} required />
        {errors.region && <p className="text-red-500">{errors.region}</p>}
      </div>
    </div>

    {agentType === 'user' && (
      <div className="grid grid-cols-2 gap-4">
        <div>
          <Label htmlFor="nickname">Nickname</Label>
          <Input id="nickname" name="nickname" value={formData.nickname} onChange={handleInputChange} />
        </div>
        <div className="flex items-center space-x-2">
          <Switch 
            id="public_profile" 
            checked={formData.public_profile} 
            onCheckedChange={(checked) => handleSelectChange('public_profile', checked)} 
          />
          <Label htmlFor="public_profile">Public Profile</Label>
        </div>
      </div>
    )}

    <div>
      <Label htmlFor="short_bio">Short Bio</Label>
      <Textarea id="short_bio" name="short_bio" value={formData.short_bio} onChange={handleInputChange} />
    </div>

    <div>
      <Label htmlFor="bio">Full Bio</Label>
      <Textarea id="bio" name="bio" value={formData.bio} onChange={handleInputChange} />
    </div>

    <div>
      <Label htmlFor="business_name">Business Name</Label>
      <Input id="business_name" name="business_name" value={formData.business_name} onChange={handleInputChange} />
    </div>

    <div>
      <Label htmlFor="website">Website</Label>
      <Input id="website" name="website" type="url" value={formData.website} onChange={handleInputChange} />
    </div>

    <div>
      <Label htmlFor="instagram_link">Instagram Link</Label>
      <Input id="instagram_link" name="instagram_link" type="url" value={formData.instagram_link} onChange={handleInputChange} />
    </div>

    {agentType === 'user' && (
      <div>
        <Label htmlFor="sustainability_practices">Sustainability Practices</Label>
        <Textarea id="sustainability_practices" name="sustainability_practices" value={formData.sustainability_practices} onChange={handleInputChange} />
      </div>
    )}

    <div className="flex items-center space-x-2">
      <Switch 
        id="hotel_owner" 
        checked={formData.hotel_owner} 
        onCheckedChange={(checked) => handleSelectChange('hotel_owner', checked)} 
      />
      <Label htmlFor="hotel_owner">Hotel Owner</Label>
    </div>

    {agentType === 'user' && (
      <>
        <div>
          <Label htmlFor="accompanying_agent">Accompanying Agent</Label>
          <SearchInput
            placeholder="Search for an agent..."
            onItemSelect={handleAgentSelect}
            isLoading={isLoadingAgents}
            data={allAgents}
            label={(agent) => `${agent.first_name} ${agent.last_name}`}
            searchFields={['first_name', 'last_name', 'username']}
            idField="id"
            selectedValue={selectedAgentId}
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <Label htmlFor="join_date">Join Date</Label>
            <Input id="join_date" name="join_date" type="date" value={formData.join_date} onChange={handleInputChange} />
          </div>
          <div>
            <Label htmlFor="agent_starting_date">Agent Starting Date</Label>
            <Input id="agent_starting_date" name="agent_starting_date" type="date" value={formData.agent_starting_date} onChange={handleInputChange} />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <Label htmlFor="default_commission_percentage">Default Commission Percentage</Label>
            <Input id="default_commission_percentage" name="default_commission_percentage" type="number" step="0.01" value={formData.default_commission_percentage} onChange={handleInputChange} />
          </div>
          <div>
            <Label htmlFor="default_organisation_fee">Default Organisation Fee</Label>
            <Input id="default_organisation_fee" name="default_organisation_fee" type="number" step="0.01" value={formData.default_organisation_fee} onChange={handleInputChange} />
          </div>
        </div>
      </>
    )}

    <div>
      <Label htmlFor="admin_description">Admin Description</Label>
      <Textarea id="admin_description" name="admin_description" value={formData.admin_description} onChange={handleInputChange} />
    </div>

    <div>
      <Label htmlFor="expertise_categories">Expertise Categories</Label>
      <MultiSelector 
        values={formData.expertise_categories} 
        onValuesChange={(values) => handleSelectChange('expertise_categories', values)}
      >
        <MultiSelectorTrigger>
          <MultiSelectorInput placeholder="Select expertise categories" />
        </MultiSelectorTrigger>
        <MultiSelectorContent>
          <MultiSelectorList>
            {expertiseCategoryOptions.map((option) => (
              <MultiSelectorItem key={option.value} value={option.value}>
                {option.label}
              </MultiSelectorItem>
            ))}
          </MultiSelectorList>
        </MultiSelectorContent>
      </MultiSelector>
    </div>
  </form>
);

return (
  <Card className="w-full max-w-4xl">
    <CardHeader>
      <CardTitle>Add an Agent</CardTitle>
      <CardDescription>Fill out the details to create a new agent account.</CardDescription>
    </CardHeader>
    <CardContent>
      <Tabs defaultValue="user" onValueChange={(value) => setAgentType(value)}>
        <TabsList>
          <TabsTrigger value="user">User Agent</TabsTrigger>
          <TabsTrigger value="potential">Potential Agent</TabsTrigger>
        </TabsList>
        <TabsContent value="user">{renderForm()}</TabsContent>
        <TabsContent value="potential">{renderForm()}</TabsContent>
      </Tabs>
    </CardContent>
    <CardFooter>
      <Button type="submit" disabled={isAddingAgent || isAddingPotentialAgent} onClick={handleSubmit}>
        {isAddingAgent || isAddingPotentialAgent ? 'Adding Agent...' : 'Add Agent'}
      </Button>
    </CardFooter>
  </Card>
);}