import React, { useState, useCallback } from 'react';
import { useAddContactMutation, useAddContactCategoryMutation, useAddContactBusinessMutation, useGetContactCategoriesQuery, useGetContactBusinessesQuery, useGetAllAgentsQuery } from '../../services/api';
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { useToast } from "@/components/ui/use-toast";
import { Switch } from "@/components/ui/switch";
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card";
import SearchInput from '../ui/SearchInput';
import { MultiSelector, MultiSelectorTrigger, MultiSelectorInput, MultiSelectorContent, MultiSelectorList, MultiSelectorItem } from "@/components/ui/multiselector";

export default function AddContact() {
  const [formData, setFormData] = useState({
    name: '',
    preferred_first_name: '',
    email_address: '',
    phone_number: '',
    whatsapp_number: '',
    is_visible_to_others: false,
    daily_rate_where_appropriate: '',
    rating: '',
    categories: [],
    business: null,
    agent: null,
  });

  const [newCategory, setNewCategory] = useState('');
  const [newBusiness, setNewBusiness] = useState({
    business_name: '',
    address: '',
    gst_number: '',
    business_website: '',
    agent: null,
  });

  const [addContact, { isLoading: isAddingContact }] = useAddContactMutation();
  const [addContactCategory] = useAddContactCategoryMutation();
  const [addContactBusiness] = useAddContactBusinessMutation();
  const { data: categories, isLoading: isLoadingCategories } = useGetContactCategoriesQuery();
  const { data: businesses, isLoading: isLoadingBusinesses } = useGetContactBusinessesQuery();
  const { data: agents, isLoading: isLoadingAgents } = useGetAllAgentsQuery();
  const { toast } = useToast();

  const handleError = (error, action) => {
    console.error(`Error ${action}:`, error);
    let errorMessage = "An unexpected error occurred. Please try again.";
    
    if (error.data) {
      if (typeof error.data === 'string') {
        errorMessage = error.data;
      } else if (typeof error.data === 'object') {
        errorMessage = Object.entries(error.data)
          .map(([key, value]) => {
            if (typeof value === 'object') {
              return `${key}: ${JSON.stringify(value)}`;
            }
            return `${key}: ${value}`;
          })
          .join('\n');
      }
    } else if (error.error) {
      errorMessage = error.error;
    }

    toast({
      title: `Error ${action}`,
      description: errorMessage,
      status: "error",
      duration: 5000,
    });
  };

  const handleInputChange = (e) => {
      const { name, value, type, checked } = e.target;
      setFormData(prev => ({
        ...prev,
        [name]: type === 'checkbox' ? checked : value
      }));
    };

  const handleCategoriesChange = useCallback((selectedCategories) => {
    setFormData(prev => ({ ...prev, categories: selectedCategories }));
  }, []);


  const handleBusinessSelect = (business) => {
    setFormData(prev => ({
      ...prev,
      business: business
    }));
  };

  const handleAgentSelect = (agent) => {
    setFormData(prev => ({
      ...prev,
      agent: agent
    }));
  };

  const handleAddNewCategory = async () => {
    if (newCategory) {
      try {
        const result = await addContactCategory({ 
          name: newCategory,
          agent: formData.agent ? formData.agent.id : undefined
        }).unwrap();
        setFormData(prev => ({
          ...prev,
          categories: [...prev.categories, result]
        }));
        setNewCategory('');
        toast({
          title: "Category Added",
          description: "The new category has been successfully added.",
          status: "success"
        });
      } catch (error) {
        handleError(error, "adding category");
      }
    }
  };

  const handleAddNewBusiness = async () => {
    if (newBusiness.business_name) {
      try {
        const result = await addContactBusiness({
          ...newBusiness,
          agent: formData.agent ? formData.agent.id : undefined
        }).unwrap();
        setFormData(prev => ({
          ...prev,
          business: result
        }));
        setNewBusiness({
          business_name: '',
          address: '',
          gst_number: '',
          business_website: '',
          agent: null,
        });
        toast({
          title: "Business Added",
          description: "The new business has been successfully added.",
          status: "success"
        });
      } catch (error) {
        handleError(error, "adding business");
      }
    }
  };

const handleSubmit = async (e) => {
  e.preventDefault();
  console.log("Form data before submission:", formData);
  try {
    const contactData = {
      ...formData,
      agent: formData.agent?.id,
      categories: formData.categories.map(c => c.id), // Send array of category IDs
      business: formData.business?.id, // Send business ID
      daily_rate_where_appropriate: formData.daily_rate_where_appropriate || null,
      rating: formData.rating || null,
    };

    // Remove any undefined or null fields
    Object.keys(contactData).forEach(key => 
      (contactData[key] === undefined || contactData[key] === null) && delete contactData[key]
    );

    console.log("Data being sent to the backend:", contactData);

    const result = await addContact(contactData).unwrap();
    console.log("Response from backend:", result);

    toast({
      title: "Contact Added",
      description: "The new contact has been successfully added.",
      status: "success"
    });

    // Reset form
    setFormData({
      name: '',
      preferred_first_name: '',
      email_address: '',
      phone_number: '',
      whatsapp_number: '',
      is_visible_to_others: false,
      daily_rate_where_appropriate: '',
      rating: '',
      categories: [],
      business: null,
      agent: null,
    });

  } catch (error) {
    console.error("Error submitting form:", error);
    handleError(error, "adding contact");
  }
};

  return (
    <Card className="w-full max-w-4xl">
      <CardHeader>
        <CardTitle>Add a Contact</CardTitle>
        <CardDescription>Fill out the details to add a new contact.</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <Label htmlFor="agent">Agent (Optional)</Label>
            <SearchInput
              placeholder="Select an agent..."
              searchPlaceholder="Search agents..."
              notFoundMessage="No agent found."
              itemType="agent"
              onItemSelect={handleAgentSelect}
              isLoading={isLoadingAgents}
              data={agents}
              label={(agent) => `${agent.first_name} ${agent.last_name}`}
              searchFields={['first_name', 'last_name', 'email']}
              idField="id"
              selectedValue={formData.agent ? formData.agent.id : null}
            />
          </div>
          <div>
            <Label htmlFor="name">Name</Label>
            <Input id="name" name="name" value={formData.name} onChange={handleInputChange} required />
          </div>
          <div>
            <Label htmlFor="preferred_first_name">Preferred First Name</Label>
            <Input id="preferred_first_name" name="preferred_first_name" value={formData.preferred_first_name} onChange={handleInputChange} />
          </div>
          <div>
            <Label htmlFor="email_address">Email Address</Label>
            <Input id="email_address" name="email_address" type="email" value={formData.email_address} onChange={handleInputChange} required />
          </div>
          <div>
            <Label htmlFor="phone_number">Phone Number</Label>
            <Input id="phone_number" name="phone_number" value={formData.phone_number} onChange={handleInputChange} required />
          </div>
          <div>
            <Label htmlFor="whatsapp_number">WhatsApp Number</Label>
            <Input id="whatsapp_number" name="whatsapp_number" value={formData.whatsapp_number} onChange={handleInputChange} />
          </div>
          <div className="flex items-center space-x-2">
            <Switch 
              id="is_visible_to_others" 
              checked={formData.is_visible_to_others} 
              onCheckedChange={(checked) => setFormData(prev => ({ ...prev, is_visible_to_others: checked }))} 
            />
            <Label htmlFor="is_visible_to_others">Visible to Others</Label>
          </div>
          <div>
            <Label htmlFor="daily_rate_where_appropriate">Daily Rate</Label>
            <Input id="daily_rate_where_appropriate" name="daily_rate_where_appropriate" type="number" value={formData.daily_rate_where_appropriate} onChange={handleInputChange} />
          </div>
          <div>
            <Label htmlFor="rating">Rating</Label>
            <Input id="rating" name="rating" type="number" min="1" max="5" value={formData.rating} onChange={handleInputChange} />
          </div>
          <div>
            <Label>Categories</Label>
            <MultiSelector 
              values={formData.categories} 
              onValuesChange={handleCategoriesChange}
            >
              <MultiSelectorTrigger>
                <MultiSelectorInput placeholder="Select categories" />
              </MultiSelectorTrigger>
              <MultiSelectorContent>
                <MultiSelectorList>
                  {categories?.map((category) => (
                    <MultiSelectorItem key={category.id} value={category.id}>
                      {category.name}
                    </MultiSelectorItem>
                  ))}
                </MultiSelectorList>
              </MultiSelectorContent>
            </MultiSelector>
            <div className="flex mt-2">
              <Input value={newCategory} onChange={(e) => setNewCategory(e.target.value)} placeholder="New category name" />
              <Button type="button" onClick={handleAddNewCategory}>Add</Button>
            </div>
          </div>
          <div>
            <Label>Business</Label>
            <SearchInput
              placeholder="Select business..."
              searchPlaceholder="Search businesses..."
              notFoundMessage="No business found."
              itemType="business"
              onItemSelect={handleBusinessSelect}
              isLoading={isLoadingBusinesses}
              data={businesses}
              label={(business) => business.business_name}
              searchFields={['business_name']}
              idField="id"
              selectedValue={formData.business ? formData.business.id : null}
            />
            <div className="space-y-2 mt-2">
              <Input value={newBusiness.business_name} onChange={(e) => setNewBusiness(prev => ({ ...prev, business_name: e.target.value }))} placeholder="New business name" />
              <Input value={newBusiness.address} onChange={(e) => setNewBusiness(prev => ({ ...prev, address: e.target.value }))} placeholder="Address" />
              <Input value={newBusiness.gst_number} onChange={(e) => setNewBusiness(prev => ({ ...prev, gst_number: e.target.value }))} placeholder="GST Number" />
              <Input value={newBusiness.business_website} onChange={(e) => setNewBusiness(prev => ({ ...prev, business_website: e.target.value }))} placeholder="Website" />
              <Button type="button" onClick={handleAddNewBusiness}>Add New Business</Button>
            </div>
          </div>
        </form>
      </CardContent>
      <CardFooter>
        <Button type="submit" onClick={handleSubmit} disabled={isAddingContact}>
          {isAddingContact ? 'Adding Contact...' : 'Add Contact'}
        </Button>
      </CardFooter>
    </Card>
  );
}