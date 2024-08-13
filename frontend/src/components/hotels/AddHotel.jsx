
import React, { useState, useCallback, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Switch } from "@/components/ui/switch";
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select";
import { useToast } from "@/components/ui/use-toast";
import SearchInput from '../ui/SearchInput';
import {
  MultiSelector,
  MultiSelectorTrigger,
  MultiSelectorInput,
  MultiSelectorContent,
  MultiSelectorList,
  MultiSelectorItem,
} from "@/components/ui/multiselector";
import { useAddCustomizedHotelMutation, useGetAllAgentsQuery, useGetRegionsQuery } from '../../services/api';

// Dummy data for tags (assuming this isn't fetched from the backend)
const tagOptions = [
  { value: 'family-friendly', label: 'Family Friendly' },
  { value: 'pet-friendly', label: 'Pet Friendly' },
  { value: 'spa', label: 'Spa' },
  { value: 'beach', label: 'Beach' },
  { value: 'mountain', label: 'Mountain' },
  { value: 'historic', label: 'Historic' },
];

export default function AddHotel() {
  const [formData, setFormData] = useState({
    name: '',
    type: '',
    region: '',
    description: '',
    platform_hotel: false,
    phone_number: '',
    whatsapp_number: '',
    email: '',
    website: '',
    instagram_link: '',
    booking_com_url: '',
    tripadvisor_url: '',
    google_place_id: '',
    min_price_in_INR: '',
    is_active: true,
    tags: [],
    hotel_owner: null
  });

  const [errors, setErrors] = useState({});
  const [filteredAgents, setFilteredAgents] = useState([]);
  const { data: allAgents, isLoading: isLoadingAgents, error: agentLoadError } = useGetAllAgentsQuery();
  const { data: regions, isLoading: isLoadingRegions } = useGetRegionsQuery();

  const [addHotel, { isLoading: isAddingHotel }] = useAddCustomizedHotelMutation();
  const { toast } = useToast();

  useEffect(() => {
    if (allAgents) {
      setFilteredAgents(allAgents);
      console.log('All agents loaded:', allAgents);
    }
  }, [allAgents]);

  const handleSearch = useCallback((searchTerm) => {
    if (!allAgents) return;
    const filtered = allAgents.filter((agent) =>
      `${agent.first_name} ${agent.last_name} ${agent.agent_profile?.business_name || ''}`
        .toLowerCase()
        .includes(searchTerm.toLowerCase())
    );
    setFilteredAgents(filtered);
    console.log('Filtered agents:', filtered);
  }, [allAgents]);

const validateForm = () => {
  let newErrors = {};
  if (!formData.name) newErrors.name = "Name is required";
  if (!formData.type) newErrors.type = "Type is required";
  if (!formData.region) newErrors.region = "Region is required";
  if (!formData.description) newErrors.description = "Description is required";
  if (formData.email && !/^\S+@\S+\.\S+$/.test(formData.email)) newErrors.email = "Invalid email format";
  if (formData.min_price_in_INR && isNaN(formData.min_price_in_INR)) newErrors.min_price_in_INR = "Price must be a number";
  if (formData.min_price_in_INR && formData.min_price_in_INR < 0) newErrors.min_price_in_INR = "Price must be non-negative";
  
  const phoneRegex = /^\+?[1-9]\d{1,14}$/;
  if (formData.phone_number && !phoneRegex.test(formData.phone_number)) newErrors.phone_number = "Invalid phone number format";
  if (formData.whatsapp_number && !phoneRegex.test(formData.whatsapp_number)) newErrors.whatsapp_number = "Invalid WhatsApp number format";

  setErrors(newErrors);
  return newErrors;
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

  const resetForm = useCallback(() => {
    setFormData({
      name: '',
      type: '',
      region: '',
      description: '',
      platform_hotel: false,
      phone_number: '',
      whatsapp_number: '',
      email: '',
      website: '',
      instagram_link: '',
      booking_com_url: '',
      tripadvisor_url: '',
      google_place_id: '',
      min_price_in_INR: '',
      is_active: true,
      tags: [],
      hotel_owner: null
    });
    setErrors({});
  }, []);

const handleSubmit = async (event) => {
  event.preventDefault();
  console.log(formData)
  const validationErrors = validateForm();
  if (Object.keys(validationErrors).length > 0) {
    const errorMessages = Object.values(validationErrors).join(', ');
    toast({
      title: "Validation Error",
      description: errorMessages,
      status: "error"
    });
    return;
  }
  try {
    const result = await addHotel(formData).unwrap();
    console.log('Hotel added successfully:', result);
    toast({
      title: "Hotel Added",
      description: "The hotel has been successfully added.",
      status: "success"
    });
    resetForm();
  } catch (error) {
    console.error('Failed to add hotel:', error);
    toast({
      title: "Error",
      description: error.data?.detail || "Failed to add hotel. Please try again.",
      status: "error"
    });
  }
};

  const handleAgentSelect = useCallback((agent) => {
    console.log('Selected agent:', agent);
    setFormData(prev => ({ ...prev, hotel_owner: agent.id }));
  }, []);

  const handleTagsChange = useCallback((selectedTags) => {
    setFormData(prev => ({ ...prev, tags: selectedTags }));
  }, []);

  return (
    <Card className="w-full max-w-4xl">
      <CardHeader>
        <CardTitle>Add a Hotel</CardTitle>
        <CardDescription>Fill out the details for a new hotel listing.</CardDescription>
      </CardHeader> 
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label htmlFor="name">Hotel Name</Label>
              <Input id="name" name="name" value={formData.name} onChange={handleInputChange} required />
              {errors.name && <p className="text-red-500">{errors.name}</p>}
            </div>
            <div>
              <Label htmlFor="type">Hotel Type</Label>
              <Select onValueChange={(value) => handleSelectChange('type', value)} value={formData.type}>
                <SelectTrigger>
                  <SelectValue placeholder="Select hotel type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="farmstay">Farmstay</SelectItem>
                  <SelectItem value="beach">Beach</SelectItem>
                  <SelectItem value="jungle">Wildlife and Jungle Lodges</SelectItem>
                  <SelectItem value="private villas">Private Villas</SelectItem>
                  <SelectItem value="wellness retreats">Wellness Retreats</SelectItem>
                  <SelectItem value="mountain stays">Mountain Stays</SelectItem>
                  <SelectItem value="hiking lodge">Hiking Lodge</SelectItem>
                </SelectContent>
              </Select>
              {errors.type && <p className="text-red-500">{errors.type}</p>}
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
             <div>
                <Label htmlFor="region">Region</Label>
                <Select 
                  id="region" 
                  value={formData.region} 
                  onValueChange={(value) => handleSelectChange('region', value)}
                >
                 <SelectTrigger>
                   <SelectValue placeholder="Select region" />
                 </SelectTrigger>
                 <SelectContent>
                    {isLoadingRegions ? (
                      <SelectItem value="">Loading regions...</SelectItem>
                    ) : (
                      regions?.map((region) => (
                        <SelectItem key={region.id} value={region.id.toString()}>
                          {region.name}
                        </SelectItem>
                      ))
                    )}
                  </SelectContent>
                </Select>
              {errors.region && <p className="text-red-500">{errors.region}</p>}
             </div>
             <div>
               <Label htmlFor="description">Description</Label>
               <Textarea id="description" name="description" value={formData.description} onChange={handleInputChange} />
             </div>
           </div>

           <div className="flex items-center space-x-2">
             <Switch 
              id="platform_hotel" 
              checked={formData.platform_hotel} 
              onCheckedChange={(checked) => handleSelectChange('platform_hotel', checked)} 
            />
            <Label htmlFor="platform_hotel">Platform Hotel</Label>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label htmlFor="phone_number">Phone Number</Label>
              <Input id="phone_number" name="phone_number" value={formData.phone_number} onChange={handleInputChange} />
              {errors.phone_number && <p className="text-red-500">{errors.phone_number}</p>}
            </div>
            <div>
              <Label htmlFor="whatsapp_number">WhatsApp Number</Label>
              <Input id="whatsapp_number" name="whatsapp_number" value={formData.whatsapp_number} onChange={handleInputChange} />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label htmlFor="email">Email Address</Label>
              <Input id="email" name="email" type="email" value={formData.email} onChange={handleInputChange} />
            </div>
            <div>
              <Label htmlFor="website">Hotel Website</Label>
              <Input id="website" name="website" type="url" value={formData.website} onChange={handleInputChange} />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label htmlFor="instagram_link">Instagram Link</Label>
              <Input id="instagram_link" name="instagram_link" value={formData.instagram_link} onChange={handleInputChange} />
            </div>
            <div>
              <Label htmlFor="booking_com_url">Booking.com URL</Label>
              <Input id="booking_com_url" name="booking_com_url" type="url" value={formData.booking_com_url} onChange={handleInputChange} />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label htmlFor="google_place_id">Google Place ID</Label>
              <Input id="google_place_id" name="google_place_id" value={formData.google_place_id} onChange={handleInputChange} />
            </div>
            <div>
              <Label htmlFor="tripadvisor_url">TripAdvisor URL</Label>
              <Input id="tripadvisor_url" name="tripadvisor_url" type="url" value={formData.tripadvisor_url} onChange={handleInputChange} />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label htmlFor="min_price_in_INR">Minimum Price (INR)</Label>
              <Input id="min_price_in_INR" name="min_price_in_INR" type="number" value={formData.min_price_in_INR} onChange={handleInputChange} />
            </div>
            <div className="flex items-center space-x-2">
              <Switch 
                id="is_active" 
                checked={formData.is_active} 
                onCheckedChange={(checked) => handleSelectChange('is_active', checked)} 
              />
              <Label htmlFor="is_active">Active</Label>
            </div>
          </div>
          <div>
            <Label htmlFor="hotel_owner">Hotel Owner</Label>
            <SearchInput
              placeholder="Search for an agent..."
              onSearch={handleSearch}
              onItemSelect={handleAgentSelect} // This now matches the prop name in SearchInput
              isLoading={isLoadingAgents}
              data={filteredAgents}
              label={(agent) => `${agent.first_name} ${agent.last_name} - ${agent.agent_profile?.business_name || ''}`}
              searchFields={['first_name', 'last_name', 'agent_profile.business_name']}
              idField="id"
            />
            {agentLoadError && <p className="text-red-500">Error loading agents: {agentLoadError.message}</p>}
          </div>
          <div>
            <Label htmlFor="tags">Tags</Label>
            <MultiSelector values={formData.tags} onValuesChange={handleTagsChange}>
              <MultiSelectorTrigger>
                <MultiSelectorInput placeholder="Select tags" />
              </MultiSelectorTrigger>
              <MultiSelectorContent>
                <MultiSelectorList>
                  {tagOptions.map((option) => (
                    <MultiSelectorItem key={option.value} value={option.value}>
                      {option.label}
                    </MultiSelectorItem>
                  ))}
                </MultiSelectorList>
              </MultiSelectorContent>
            </MultiSelector>
          </div>
        </form>
      </CardContent>
      <CardFooter>
        <Button type="submit" onClick={handleSubmit} disabled={isAddingHotel}>
          {isAddingHotel ? 'Adding Hotel...' : 'Add Hotel'}
        </Button>
      </CardFooter>
    </Card>
  );
}

// Version 2 - without backend connection



// import React, { useState } from 'react';
// import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card";
// import { Label } from "@/components/ui/label";
// import { Input } from "@/components/ui/input";
// import { Button } from "@/components/ui/button";
// import { Textarea } from "@/components/ui/textarea";
// import { Switch } from "@/components/ui/switch";
// import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select";
// import { useToast } from "@/components/ui/use-toast";
// import SearchInput from '../ui/SearchInput';
// import {
//   MultiSelector,
//   MultiSelectorTrigger,
//   MultiSelectorInput,
//   MultiSelectorContent,
//   MultiSelectorList,
//   MultiSelectorItem,
// } from "@/components/ui/multiselector";



// // import { useAddHotelMutation, useSearchAgentsQuery } from '../../services/api';
// // import AddAgent from '../users/AddAgent'; AFTER - ADD MODAL ADDAGTN



// // Dummy data for agents
// const dummyAgents = [
//   { id: 1, first_name: 'John', last_name: 'Doe', agent_profile: { business_name: 'Johns Agency' } },
//   { id: 2, first_name: 'Jane', last_name: 'Smith', agent_profile: { business_name: 'Janes Tours' } },
//   { id: 3, first_name: 'Bob', last_name: 'Johnson', agent_profile: { business_name: 'Bobs Travels' } },
// ];

// // Dummy data for tags
// const tagOptions = [
//   { value: 'family-friendly', label: 'Family Friendly' },
//   { value: 'pet-friendly', label: 'Pet Friendly' },
//   { value: 'spa', label: 'Spa' },
//   { value: 'beach', label: 'Beach' },
//   { value: 'mountain', label: 'Mountain' },
//   { value: 'historic', label: 'Historic' },
// ];

// export default function AddHotel() {
//   const [formData, setFormData] = useState({
//     name: '',
//     type: '',
//     region: '',
//     description: '',
//     platform_hotel: false,
//     phone_number: '',
//     whatsapp_number: '',
//     email: '',
//     website: '',
//     instagram_link: '',
//     booking_com_url: '',
//     tripadvisor_url: '',
//     google_place_id: '',
//     min_price_in_INR: '',
//     is_active: true,
//     tags: [],
//     hotel_owner: null
//   });

//   const { toast } = useToast();

//   const handleInputChange = (e) => {
//     const { name, value, type, checked } = e.target;
//     setFormData(prev => ({
//       ...prev,
//       [name]: type === 'checkbox' ? checked : value
//     }));
//   };

//   const handleSelectChange = (name, value) => {
//     setFormData(prev => ({ ...prev, [name]: value }));
//   };

//   const handleAgentSelect = (selectedAgent) => {
//     setFormData(prev => ({ ...prev, hotel_owner: selectedAgent.id }));
//   };

//   const handleTagsChange = (selectedTags) => {
//     setFormData(prev => ({ ...prev, tags: selectedTags }));
//   };

//   const handleSubmit = (event) => {
//     event.preventDefault();
//     console.log('Submitting hotel data:', formData);
//     toast({
//       title: "Form Submitted",
//       description: "Hotel data has been submitted successfully.",
//     });
//   };

//   return (
//     <Card className="w-full max-w-4xl">
//       <CardHeader>
//         <CardTitle>Add a Hotel</CardTitle>
//         <CardDescription>Fill out the details for a new hotel listing.</CardDescription>
//       </CardHeader>
//       <CardContent>
//         <form onSubmit={handleSubmit} className="space-y-4">
//           <div className="grid grid-cols-2 gap-4">
//             <div>
//               <Label htmlFor="name">Hotel Name</Label>
//               <Input id="name" name="name" value={formData.name} onChange={handleInputChange} required />
//             </div>
//             <div>
//               <Label htmlFor="type">Hotel Type</Label>
//               <Select onValueChange={(value) => handleSelectChange('type', value)} value={formData.type}>
//                 <SelectTrigger>
//                   <SelectValue placeholder="Select hotel type" />
//                 </SelectTrigger>
//                 <SelectContent>
//                   <SelectItem value="farmstay">Farmstay</SelectItem>
//                   <SelectItem value="beach">Beach</SelectItem>
//                   <SelectItem value="jungle">Wildlife and Jungle Lodges</SelectItem>
//                   <SelectItem value="private villas">Private Villas</SelectItem>
//                   <SelectItem value="wellness retreats">Wellness Retreats</SelectItem>
//                   <SelectItem value="mountain stays">Mountain Stays</SelectItem>
//                   <SelectItem value="hiking lodge">Hiking Lodge</SelectItem>
//                 </SelectContent>
//               </Select>
//             </div>
//           </div>

//           <div className="grid grid-cols-2 gap-4">
//             <div>
//               <Label htmlFor="region">Region</Label>
//               <Select onValueChange={(value) => handleSelectChange('region', value)} value={formData.region}>
//                 <SelectTrigger>
//                   <SelectValue placeholder="Select region" />
//                 </SelectTrigger>
//                 <SelectContent>
//                   <SelectItem value="ladakh">Ladakh</SelectItem>
//                   <SelectItem value="goa">Goa</SelectItem>
//                   <SelectItem value="kerala">Kerala</SelectItem>
//                   <SelectItem value="himachal-pradesh">Himachal Pradesh</SelectItem>
//                   <SelectItem value="kashmir">Kashmir</SelectItem>
//                   <SelectItem value="rajasthan">Rajasthan</SelectItem>
//                   <SelectItem value="delhi">Delhi</SelectItem>
//                 </SelectContent>
//               </Select>
//             </div>
//             <div>
//               <Label htmlFor="description">Description</Label>
//               <Textarea id="description" name="description" value={formData.description} onChange={handleInputChange} />
//             </div>
//           </div>

//           <div className="flex items-center space-x-2">
//             <Switch 
//               id="platform_hotel" 
//               checked={formData.platform_hotel} 
//               onCheckedChange={(checked) => handleSelectChange('platform_hotel', checked)} 
//             />
//             <Label htmlFor="platform_hotel">Platform Hotel</Label>
//           </div>

//           <div className="grid grid-cols-2 gap-4">
//             <div>
//               <Label htmlFor="phone_number">Phone Number</Label>
//               <Input id="phone_number" name="phone_number" value={formData.phone_number} onChange={handleInputChange} />
//             </div>
//             <div>
//               <Label htmlFor="whatsapp_number">WhatsApp Number</Label>
//               <Input id="whatsapp_number" name="whatsapp_number" value={formData.whatsapp_number} onChange={handleInputChange} />
//             </div>
//           </div>

//           <div className="grid grid-cols-2 gap-4">
//             <div>
//               <Label htmlFor="email">Email Address</Label>
//               <Input id="email" name="email" type="email" value={formData.email} onChange={handleInputChange} />
//             </div>
//             <div>
//               <Label htmlFor="website">Hotel Website</Label>
//               <Input id="website" name="website" type="url" value={formData.website} onChange={handleInputChange} />
//             </div>
//           </div>

//           <div className="grid grid-cols-2 gap-4">
//             <div>
//               <Label htmlFor="instagram_link">Instagram Link</Label>
//               <Input id="instagram_link" name="instagram_link" value={formData.instagram_link} onChange={handleInputChange} />
//             </div>
//             <div>
//               <Label htmlFor="booking_com_url">Booking.com URL</Label>
//               <Input id="booking_com_url" name="booking_com_url" type="url" value={formData.booking_com_url} onChange={handleInputChange} />
//             </div>
//           </div>

//           <div className="grid grid-cols-2 gap-4">
//             <div>
//               <Label htmlFor="google_place_id">Google Place ID</Label>
//               <Input id="google_place_id" name="google_place_id" value={formData.google_place_id} onChange={handleInputChange} />
//             </div>
//             <div>
//               <Label htmlFor="tripadvisor_url">TripAdvisor URL</Label>
//               <Input id="tripadvisor_url" name="tripadvisor_url" type="url" value={formData.tripadvisor_url} onChange={handleInputChange} />
//             </div>
//           </div>

//           <div className="grid grid-cols-2 gap-4">
//             <div>
//               <Label htmlFor="min_price_in_INR">Minimum Price (INR)</Label>
//               <Input id="min_price_in_INR" name="min_price_in_INR" type="number" value={formData.min_price_in_INR} onChange={handleInputChange} />
//             </div>
//             <div className="flex items-center space-x-2">
//               <Switch 
//                 id="is_active" 
//                 checked={formData.is_active} 
//                 onCheckedChange={(checked) => handleSelectChange('is_active', checked)} 
//               />
//               <Label htmlFor="is_active">Active</Label>
//             </div>
//           </div>

//           <div>
//             <Label htmlFor="hotel_owner">Hotel Owner</Label>
//             <SearchInput 
//               data={dummyAgents}
//               onSelect={handleAgentSelect}
//               placeholder="Select agent..."
//               label={(agent) => `${agent.first_name} ${agent.last_name} - ${agent.agent_profile.business_name}`}
//               searchFields={['first_name', 'last_name', 'agent_profile.business_name']}
//               idField="id"
//             />
//           </div>

//           <div>
//             <Label htmlFor="tags">Tags</Label>
//             <MultiSelector values={formData.tags} onValuesChange={handleTagsChange}>
//               <MultiSelectorTrigger>
//                 <MultiSelectorInput placeholder="Select tags" />
//               </MultiSelectorTrigger>
//               <MultiSelectorContent>
//                 <MultiSelectorList>
//                   {tagOptions.map((option) => (
//                     <MultiSelectorItem key={option.value} value={option.value}>
//                       {option.label}
//                     </MultiSelectorItem>
//                   ))}
//                 </MultiSelectorList>
//               </MultiSelectorContent>
//             </MultiSelector>
//           </div>
//         </form>
//       </CardContent>
//       <CardFooter>
//         <Button type="submit" onClick={handleSubmit}>
//           Add Hotel
//         </Button>
//       </CardFooter>
//     </Card>
//   );
// }


// export default function AddHotel() {
//   const [formData, setFormData] = useState({
//     name: '',
//     type: '',
//     region: '',
//     description: '',
//     platform_hotel: false,
//     phone_number: '',
//     whatsapp_number: '',
//     email: '',
//     website: '',
//     instagram_link: '',
//     booking_com_url: '',
//     tripadvisor_url: '',
//     google_place_id: '',
//     min_price_in_INR: '',
//     is_active: true,
//     tags: [],
//     hotel_owner: null
//   });

//   const [errors, setErrors] = useState({});
//   const [searchTerm, setSearchTerm] = useState('');
//   const { data: agents, isLoading: isLoadingAgents, error: agentSearchError } = useSearchAgentsQuery(searchTerm, {
//     skip: searchTerm.length < 2,
//     refetchOnMountOrArgChange: true
//   });



//   const [addHotel, { isLoading: isAddingHotel }] = useAddHotelMutation();
//   const { toast } = useToast();

//   useEffect(() => {
//     console.log('Search Term:', searchTerm);
//     console.log('Agents:', agents);
//     console.log('Is Loading Agents:', isLoadingAgents);
//     console.log('Agent Search Error:', agentSearchError);
//   }, [searchTerm, agents, isLoadingAgents, agentSearchError]);

//   const validateForm = () => {
//     let newErrors = {};
//     if (!formData.name) newErrors.name = "Name is required";
//     if (!formData.type) newErrors.type = "Type is required";
//     if (!formData.region) newErrors.region = "Region is required";
//     if (!formData.description) newErrors.description = "Description is required";
//     if (formData.email && !/^\S+@\S+\.\S+$/.test(formData.email)) newErrors.email = "Invalid email format";
//     if (formData.min_price_in_INR && isNaN(formData.min_price_in_INR)) newErrors.min_price_in_INR = "Price must be a number";
//     if (formData.min_price_in_INR && formData.min_price_in_INR < 0) newErrors.min_price_in_INR = "Price must be non-negative";
    
//     const phoneRegex = /^\+?[1-9]\d{1,14}$/;
//     if (formData.phone_number && !phoneRegex.test(formData.phone_number)) newErrors.phone_number = "Invalid phone number format";
//     if (formData.whatsapp_number && !phoneRegex.test(formData.whatsapp_number)) newErrors.whatsapp_number = "Invalid WhatsApp number format";

//     setErrors(newErrors);
//     return Object.keys(newErrors).length === 0;
//   };

//   const handleInputChange = (e) => {
//     const { name, value, type, checked } = e.target;
//     setFormData(prev => ({
//       ...prev,
//       [name]: type === 'checkbox' ? checked : value
//     }));
//   };

//   const handleSelectChange = (name, value) => {
//     setFormData(prev => ({ ...prev, [name]: value }));
//   };

//   const handleSubmit = async (event) => {
//     event.preventDefault();
//     if (!validateForm()) {
//       toast({
//         title: "Validation Error",
//         description: "Please correct the errors in the form.",
//         status: "error"
//       });
//       return;
//     }
//     try {
//       const result = await addHotel(formData).unwrap();
//       console.log('Hotel added successfully:', result);
//       toast({
//         title: "Hotel Added",
//         description: "The hotel has been successfully added.",
//         status: "success"
//       });
//       // Reset form or redirect
//     } catch (error) {
//       console.error('Failed to add hotel:', error);
//       toast({
//         title: "Error",
//         description: error.data?.detail || "Failed to add hotel. Please try again.",
//         status: "error"
//       });
//     }
//   };


//   const renderAgent = (agent) => {
//     const displayName = agent.nickname || agent.first_name || '';
//     const lastName = agent.last_name || '';
//     const businessName = agent.agent_profile?.business_name || '';

//     let fullName = displayName;
//     if (lastName) fullName += ` ${lastName}`;

//     return (
//       <div>
//         <span className="font-semibold">
//           {fullName}
//           {businessName && fullName && ' - '}
//           {businessName}
//         </span>
//       </div>
//     );
//   };

//   const handleSearch = useCallback((query) => {
//     console.log('Search query:', query);
//     setSearchTerm(query);
//   }, []);
  
//   const handleTagsChange = (selectedTags) => {
//     setFormData(prev => ({ ...prev, tags: selectedTags }));
//   };
  
//   const handleAgentSelect = (agent) => {
//     console.log('Selected agent:', agent);
//     setFormData(prev => ({ ...prev, hotel_owner: agent.id }));
//   };

//   console.log('Agents:', agents);
//   console.log('Is Loading Agents:', isLoadingAgents);
//   console.log('Agent Search Error:', agentSearchError);

//   return (
//     <Card className="w-full max-w-4xl">
//       <CardHeader>
//         <CardTitle>Add a Hotel</CardTitle>
//         <CardDescription>Fill out the details for a new hotel listing.</CardDescription>
//       </CardHeader>
//       <CardContent>
//         <form onSubmit={handleSubmit} className="grid gap-6">
//           <div className="grid grid-cols-2 gap-6">
//             <div className="grid gap-2">
//               <Label htmlFor="name">Hotel Name</Label>
//               <Input id="name" name="name" value={formData.name} onChange={handleInputChange} required />
//               {errors.name && <p className="text-red-500">{errors.name}</p>}
//             </div>
//             <div className="grid gap-2">
//               <Label htmlFor="type">Hotel Type</Label>
//               <Select onValueChange={(value) => handleSelectChange('type', value)} value={formData.type || undefined}>
//                 <SelectTrigger>
//                   <SelectValue placeholder="Select hotel type" />
//                 </SelectTrigger>
//                 <SelectContent>
//                   <SelectItem value="farmstay">Farmstay</SelectItem>
//                   <SelectItem value="beach">Beach</SelectItem>
//                   <SelectItem value="jungle">Wildlife and Jungle Lodges</SelectItem>
//                   <SelectItem value="private villas">Private Villas</SelectItem>
//                   <SelectItem value="wellness retreats">Wellness Retreats</SelectItem>
//                   <SelectItem value="mountain stays">Mountain Stays</SelectItem>
//                   <SelectItem value="hiking lodge">Hiking Lodge</SelectItem>
//                 </SelectContent>
//               </Select>
//               {errors.type && <p className="text-red-500">{errors.type}</p>}
//             </div>
//           </div>
//           <div className="grid grid-cols-2 gap-6">
//             <div className="grid gap-2">
//               <Label htmlFor="region">Region</Label>
//               <Select id="region">
//                 <SelectTrigger>
//                   <SelectValue placeholder="Select region" />
//                 </SelectTrigger>
//                 <SelectContent>
//                   <SelectItem value="ladakh">Ladakh</SelectItem>
//                   <SelectItem value="goa">Goa</SelectItem>
//                   <SelectItem value="kerala">Kerala</SelectItem>
//                   <SelectItem value="himachal-pradesh">Himachal Pradesh</SelectItem>
//                   <SelectItem value="kashmir">Kashmir</SelectItem>
//                   <SelectItem value="rajasthan">Rajasthan</SelectItem>
//                   <SelectItem value="delhi">Delhi</SelectItem>
//                 </SelectContent>
//               </Select>
//             </div>
//             <div className="grid gap-2">
//               <Label htmlFor="description">Description</Label>
//               <Textarea id="description" name="description" value={formData.description} onChange={handleInputChange} required />
//               {errors.description && <p className="text-red-500">{errors.description}</p>}
//             </div>
//             <div className="flex items-center gap-2">
//               <Switch id="platform_hotel" name="platform_hotel" checked={formData.platform_hotel} onCheckedChange={(checked) => handleSelectChange('platform_hotel', checked)} />
//               <Label htmlFor="platform_hotel">Platform Hotel</Label>
//             </div>
//             <div className="grid grid-cols-2 gap-6">
//               <div className="grid gap-2">
//                 <Label htmlFor="phone">Phone Number</Label>
//                 <Input id="phone" name="phone_number" type="tel" placeholder="Enter phone number" value={formData.phone_number} onChange={handleInputChange} />
//                 {errors.phone_number && <p className="text-red-500">{errors.phone_number}</p>}
//               </div>
//               <div className="grid gap-2">
//                 <Label htmlFor="whatsapp">WhatsApp Number</Label>
//                 <Input id="whatsapp" name="whatsapp_number" type="tel" placeholder="Enter WhatsApp number" value={formData.whatsapp_number} onChange={handleInputChange} />
//                 {errors.whatsapp_number && <p className="text-red-500">{errors.whatsapp_number}</p>}
//               </div>
//             </div>
//           </div>
//           <div className="grid grid-cols-2 gap-6">
//             <div className="grid gap-2">
//               <Label htmlFor="email">Email Address</Label>
//               <Input id="email" type="email" placeholder="Enter email address" />
//             </div>
//             <div className="grid gap-2">
//               <Label htmlFor="website">Hotel Website</Label>
//               <Input id="website" type="url" placeholder="Enter hotel website URL" />
//             </div>
//           </div>


//           <div className="grid grid-cols-2 gap-6">
//             <div className="grid gap-2">
//               <Label htmlFor="instagram">Hotel Instagram</Label>
//               <Input id="instagram" placeholder="Enter hotel Instagram handle" />
//             </div>
//             <div className="grid gap-2">
//               <Label htmlFor="booking-com">Booking.com URL</Label>
//               <Input id="booking-com" type="url" placeholder="Enter Booking.com URL" />
//             </div>
//           </div>

//           <div className="grid grid-cols-2 gap-6">
//             <div className="grid gap-2">
//               <Label htmlFor="place-id">Google Place ID</Label>
//               <Input id="place-id" placeholder="Enter Google Place ID" />
//             </div>

//             <div className="grid gap-2">
//               <Label htmlFor="tripadvisor">TripAdvisor URL</Label>
//               <Input id="tripadvisor" type="url" placeholder="Enter Tripadvisor URL" />
//             </div>
//           </div>

//           <div className="grid grid-cols-2 gap-6">
//             <div className="grid gap-2">
//               <Label htmlFor="min-price">Minimum Price (INR)</Label>
//               <Input id="min-price" type="number" placeholder="Enter minimum price" />
//             </div>
//             <div className="grid gap-2">
//               <Label htmlFor="active">Active</Label>
//               <Switch id="active" aria-label="Active" />
//             </div>
//           </div>
//          <div className="grid gap-2">
//             <Label htmlFor="hotel_owner">Hotel Owner</Label>
//           <SearchInput
//             placeholder="Search for an agent..."
//             onSearch={handleSearch}
//             isLoading={isLoadingAgents}
//             items={agents || []}
//             onItemSelect={handleAgentSelect}
//             renderItem={renderAgent}
//             addNewComponent={AddAgent}
//             addNewButtonText="Add new agent"
//             dialogTitle="Add New Agent"
//             dialogDescription="Create a new agent profile"
//           />
//           </div>

//           <div className="grid gap-2">
//             <Label htmlFor="tags">Tags</Label>
//             <MultiSelect
//               options={[
//                 { value: 'family-friendly', label: 'Family Friendly' },
//                 { value: 'pet-friendly', label: 'Pet Friendly' },
//                 { value: 'spa', label: 'Spa' },
//                 { value: 'beach', label: 'Beach' },
//                 { value: 'mountain', label: 'Mountain' },
//                 { value: 'historic', label: 'Historic' },
//               ]}
//               onChange={handleTagsChange}
//               value={formData.tags}
//             />
//           </div>

//         </form>
//       </CardContent>
//       <CardFooter>
//         <Button type="submit" onClick={handleSubmit} disabled={isAddingHotel}>
//           {isAddingHotel ? 'Adding Hotel...' : 'Add Hotel'}
//         </Button>
//       </CardFooter>
//     </Card>
//   );
// }