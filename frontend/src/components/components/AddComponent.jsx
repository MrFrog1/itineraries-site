import React, { useState, useMemo } from 'react';
import { useSelector } from 'react-redux';
import { useAddComponentMutation, useGetAllComponentTypesQuery, useGetComponentTypesQuery, useGetAllAgentsQuery, useGetContactsQuery } from '../../services/api';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Switch } from "@/components/ui/switch";
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { useToast } from "@/components/ui/use-toast";
import { Dialog, DialogTrigger, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import SearchInput from '../ui/SearchInput';
import AddComponentTypeForm from './AddComponentType';
import AddContactModal from '../contacts/AddContactModal';
import {
  MultiSelector,
  MultiSelectorTrigger,
  MultiSelectorInput,
  MultiSelectorContent,
  MultiSelectorList,
  MultiSelectorItem,
} from "@/components/ui/multiselector";


const CATEGORY_CHOICES = [
  'all', 'ironman', 'tough', 'challenging', 'moderate', 'easy'
];

export default function AddComponent() {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    component_type_id: '',
    is_platform_experience: false,
    is_visible_to_all: false,
    wheelchair_accessible: true,
    age_limit: '',
    fitness_level: '',
    price_for_1_pax: '',
    price_for_2_pax: '',
    price_for_3_pax: '',
    price_for_4_pax: '',
    fixed_price_overall: '',
    fixed_price_per_person: '',
    net_price_for_1_pax: '',
    net_price_for_2_pax: '',
    net_price_for_3_pax: '',
    net_price_for_4_pax: '',
    net_fixed_price_overall: '',
    net_fixed_price_per_person: '',
    contact_id: null,
    agent_ids: [],
    region_id: '',
  });

  // const [searchTerm, setSearchTerm] = useState("");
  const [clientPricePercentage, setClientPricePercentage] = useState(0);
  const [isAddContactModalOpen, setIsAddContactModalOpen] = useState(false);
  const [errors, setErrors] = useState({});
  const [addComponent, { isLoading: isAddingComponent }] = useAddComponentMutation();
  const [selectedAgent, setSelectedAgent] = useState(null);
  const { data: allComponentTypes, isLoading: isLoadingAllComponentTypes } = useGetAllComponentTypesQuery();
  
  const { data: agentComponentTypes, isLoading: isLoadingComponentTypes, refetch: refetchComponentTypes } = useGetComponentTypesQuery(
    selectedAgent ? selectedAgent.id : undefined,
    { skip: !selectedAgent }
  );

  // const componentTypes = selectedAgent ? agentComponentTypes : allComponentTypes;
  // const isLoadingComponentTypes = selectedAgent ? isLoadingAgentComponentTypes : isLoadingAllComponentTypes;

  const { data: agents } = useGetAllAgentsQuery();
  const { data: contacts, isLoading: isLoadingContacts, refetch: refetchContacts } = useGetContactsQuery();
  const regions = useSelector(state => state.region.regions);
  const { toast } = useToast();



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

  const handleContactAdded = async (newContact) => {
    // Refetch the contacts list
    await refetchContacts();
    
    // Update the formData with the new contact
    setFormData(prev => ({ ...prev, contact_id: newContact.id }));
    
    // Close the modal
    setIsAddContactModalOpen(false);
  };


  const handleComponentTypeAdded = async (newComponentType) => {
    if (selectedAgent) {
      await refetchComponentTypes();
    }
    setFormData(prev => ({ ...prev, component_type_id: newComponentType.id }));
  };

  const handleAgentChange = (agent) => {
    setSelectedAgent(agent);
    // Reset the selected component type when the agent changes
    setFormData(prev => ({ ...prev, component_type_id: null }));
  };


  const handleAgentSelect = (selectedAgentIds) => {
    const selectedAgent = agents.find(agent => agent.id === selectedAgentIds[0]);
    setSelectedAgent(selectedAgent);
    setFormData(prev => ({
      ...prev,
      agent_ids: selectedAgentIds,
      component_type_id: '' // Reset component type when agent changes
    }));
  };

  const handleComponentTypeSelect = (componentType) => {
    setFormData(prev => ({ ...prev, component_type_id: componentType.id }));
  };


  const handleRegionSelect = (region) => {
    setFormData(prev => ({ ...prev, region_id: region.id }));
  };



  const handlePriceChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    
    // If it's a net price field, calculate the client price
    if (name.startsWith('net_')) {
      const clientFieldName = name.replace('net_', '');
      const clientPrice = parseFloat(value) * (1 + clientPricePercentage / 100);
      setFormData(prev => ({ ...prev, [clientFieldName]: clientPrice.toFixed(2) }));
    }
  };

  const handleClientPricePercentageChange = (e) => {
    const percentage = parseFloat(e.target.value);
    setClientPricePercentage(percentage);
    
    // Recalculate all client prices
    Object.keys(formData).forEach(key => {
      if (key.startsWith('net_')) {
        const clientFieldName = key.replace('net_', '');
        const netPrice = parseFloat(formData[key]);
        if (!isNaN(netPrice)) {
          const clientPrice = netPrice * (1 + percentage / 100);
          setFormData(prev => ({ ...prev, [clientFieldName]: clientPrice.toFixed(2) }));
        }
      }
    });
  };

  const validateForm = () => {
    let newErrors = {};
    
    if (!formData.name.trim()) newErrors.name = "Name is required";
    if (!formData.description.trim()) newErrors.description = "Description is required";
    if (!formData.component_type_id) newErrors.component_type_id = "Component type is required";
    if (!formData.fitness_level) newErrors.fitness_level = "Fitness level is required";
    
    if (formData.agent_ids.length === 0 && !formData.region_id) {
      newErrors.agents = "Select at least one agent or a region";
    }

  const priceFields = [
    'price_for_1_pax', 'price_for_2_pax', 'price_for_3_pax', 'price_for_4_pax',
    'fixed_price_overall', 'fixed_price_per_person',
    'net_price_for_1_pax', 'net_price_for_2_pax', 'net_price_for_3_pax', 'net_price_for_4_pax',
    'net_fixed_price_overall', 'net_fixed_price_per_person'
  ];

  priceFields.forEach(field => {
    const value = formData[field];
    if (value !== '' && value !== null && value !== undefined) {
      const numValue = parseFloat(value);
      if (isNaN(numValue) || numValue < 0) {
        newErrors[field] = "Price must be a non-negative number";
      }
    }
  });


    if (formData.age_limit && (isNaN(formData.age_limit) || parseInt(formData.age_limit) < 0)) {
      newErrors.age_limit = "Age limit must be a non-negative number";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Form data before submission:", formData);

    if (!validateForm()) {
      const errorMessages = Object.entries(errors)
        .map(([key, value]) => `${key}: ${value}`)
        .join('\n');
      
      toast({
        title: "Validation Error",
        description: `Please correct the following errors:\n${errorMessages}`,
        status: "error",
        duration: 5000,
        isClosable: true,
      });
      return;
    }

    try {
      const componentData = {
        ...formData,
        agent_ids: formData.agent_ids.length > 0 ? formData.agent_ids : undefined,
        region_id: formData.region_id || undefined,
        contact_id: formData.contact_id || undefined,
        age_limit: formData.age_limit || null,
      };

      // Handle price fields
      const priceFields = [
        'price_for_1_pax', 'price_for_2_pax', 'price_for_3_pax', 'price_for_4_pax',
        'fixed_price_overall', 'fixed_price_per_person',
        'net_price_for_1_pax', 'net_price_for_2_pax', 'net_price_for_3_pax', 'net_price_for_4_pax',
        'net_fixed_price_overall', 'net_fixed_price_per_person'
      ];

      priceFields.forEach(field => {
        if (componentData[field] === '' || componentData[field] === null || componentData[field] === undefined) {
          delete componentData[field];
        } else {
          componentData[field] = parseFloat(componentData[field]);
        }
      });

      // Remove any undefined, null, or empty string fields
      Object.keys(componentData).forEach(key => 
        (componentData[key] === undefined || componentData[key] === null || componentData[key] === '') && delete componentData[key]
      );

      console.log("Data being sent to the backend:", componentData);

      let result;
      if (componentData.region_id) {
        // Create component for all agents in the region
        result = await addComponent({ ...componentData, create_for_region: true }).unwrap();
      } else {
        // Create component for selected agents
        result = await addComponent(componentData).unwrap();
      }

      console.log("Response from backend:", result);

      toast({
        title: "Component Added",
        description: "The component has been successfully added.",
        status: "success"
      });

      // Reset form
      setFormData({
        name: '',
        description: '',
        component_type_id: '',
        is_platform_experience: false,
        is_visible_to_all: false,
        wheelchair_accessible: true,
        age_limit: '',
        fitness_level: '',
        price_for_1_pax: '',
        price_for_2_pax: '',
        price_for_3_pax: '',
        price_for_4_pax: '',
        fixed_price_overall: '',
        fixed_price_per_person: '',
        net_price_for_1_pax: '',
        net_price_for_2_pax: '',
        net_price_for_3_pax: '',
        net_price_for_4_pax: '',
        net_fixed_price_overall: '',
        net_fixed_price_per_person: '',
        contact_id: null,
        agent_ids: [],
        region_id: '',
      });

  } catch (error) {
    console.error("Error submitting form:", error);
    
    let errorMessage = "Failed to add component. Please try again.";
    if (error.data) {
      if (typeof error.data === 'string') {
        errorMessage = error.data;
      } else if (typeof error.data === 'object') {
        errorMessage = Object.entries(error.data)
          .map(([key, value]) => `${key}: ${value}`)
          .join('\n');
      }
    } else if (error.error) {
      errorMessage = error.error;
    }

    toast({
      title: "Error",
      description: errorMessage,
      status: "error",
      duration: 5000,
      isClosable: true,
    });
  }
};


  return (
    <div className="space-y-8">
      <Card className="w-full max-w-4xl">
        <CardHeader>
          <CardTitle>Add Component Type</CardTitle>
        </CardHeader>
        <CardContent>
          <AddComponentTypeForm onComponentTypeAdded={handleComponentTypeAdded} onAgentChange={handleAgentChange}/>
        </CardContent>
      </Card>
      <div className="border-t border-gray-200 my-8"></div>

    <Card className="w-full max-w-4xl">
      <CardHeader>
        <CardTitle>Add a Component</CardTitle>
        <CardDescription>Fill out the details for a new component.</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label htmlFor="name">Component Name</Label>
              <Input id="name" name="name" value={formData.name} onChange={handleInputChange} required />
              {errors.name && <p className="text-red-500">{errors.name}</p>}
            </div>
            <div>
              <Label htmlFor="component_type_id">Component Type</Label>
              <SearchInput
                placeholder="Select a component type..."
                searchPlaceholder="Search component types..."
                notFoundMessage="No component type found."
                itemType="component type"
                onItemSelect={handleComponentTypeSelect}
                isLoading={isLoadingComponentTypes}
                data={agentComponentTypes || []}
                label={(type) => type.name}
                searchFields={['name']}
                idField="id"
                selectedValue={formData.component_type_id}
                disabled={!selectedAgent}
              />
              {!selectedAgent && <p className="text-sm text-gray-500 mt-1">Please select an agent first to view component types.</p>}
              {errors.component_type_id && <p className="text-red-500">{errors.component_type_id}</p>}
            </div>
          </div>
          <div>
            <Label htmlFor="description">Description</Label>
            <Textarea id="description" name="description" value={formData.description} onChange={handleInputChange} />
            {errors.description && <p className="text-red-500">{errors.description}</p>}
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="flex items-center space-x-2">
              <Switch 
                id="is_platform_experience" 
                checked={formData.is_platform_experience} 
                onCheckedChange={(checked) => handleSelectChange('is_platform_experience', checked)} 
              />
              <Label htmlFor="is_platform_experience">Platform Experience</Label>
            </div>
            <div className="flex items-center space-x-2">
              <Switch 
                id="is_visible_to_all" 
                checked={formData.is_visible_to_all} 
                onCheckedChange={(checked) => handleSelectChange('is_visible_to_all', checked)} 
              />
              <Label htmlFor="is_visible_to_all">Visible to All</Label>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label htmlFor="age_limit">Age Limit</Label>
              <Input id="age_limit" name="age_limit" type="number" value={formData.age_limit} onChange={handleInputChange} />
            </div>
            <div>
              <Label htmlFor="fitness_level">Fitness Level</Label>
              <Select onValueChange={(value) => handleSelectChange('fitness_level', value)} value={formData.fitness_level}>
                <SelectTrigger>
                  <SelectValue placeholder="Select fitness level" />
                </SelectTrigger>
                <SelectContent>
                  {CATEGORY_CHOICES.map((level) => (
                    <SelectItem key={level} value={level}>{level}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {errors.fitness_level && <p className="text-red-500">{errors.fitness_level}</p>}
            </div>
          </div>



            <div>
              <Label htmlFor="contact_id">Contact</Label>
              <div className="flex space-x-2">
                <SearchInput
                  placeholder="Select a contact..."
                  searchPlaceholder="Search contacts..."
                  notFoundMessage="No contact found."
                  itemType="contact"
                  onItemSelect={(contact) => setFormData(prev => ({ ...prev, contact_id: contact.id }))}
                  isLoading={isLoadingContacts}
                  data={contacts}
                  label={(contact) => contact.name}
                  searchFields={['name', 'preferred_first_name', 'email_address']}
                  idField="id"
                  selectedValue={formData.contact_id}
                />
                <Dialog open={isAddContactModalOpen} onOpenChange={setIsAddContactModalOpen}>
                  <DialogTrigger asChild>
                    <Button variant="outline">Add Contact</Button>
                  </DialogTrigger>
                  <DialogContent>
                    <DialogHeader>
                      <DialogTitle>Add New Contact</DialogTitle>
                      <DialogDescription>Enter the details for the new contact.</DialogDescription>
                    </DialogHeader>
                    <AddContactModal onClose={() => setIsAddContactModalOpen(false)} onContactAdded={handleContactAdded} />
                  </DialogContent>
                </Dialog>
              </div>
            </div>

            <div>
              <Label htmlFor="clientPricePercentage">Client Price Calculator (%)</Label>
              <Input
                id="clientPricePercentage"
                name="clientPricePercentage"
                type="number"
                value={clientPricePercentage}
                onChange={handleClientPricePercentageChange}
              />
            </div>

            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Pax</TableHead>
                  <TableHead>Client Price</TableHead>
                  <TableHead>Net Price</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {[1, 2, 3, 4].map(pax => (
                  <TableRow key={pax}>
                    <TableCell>{pax}</TableCell>
                    <TableCell>
                      <Input
                        name={`price_for_${pax}_pax`}
                        value={formData[`price_for_${pax}_pax`]}
                        onChange={handlePriceChange}
                        type="number"
                      />
                    </TableCell>
                    <TableCell>
                      <Input
                        name={`net_price_for_${pax}_pax`}
                        value={formData[`net_price_for_${pax}_pax`]}
                        onChange={handlePriceChange}
                        type="number"
                      />
                    </TableCell>
                  </TableRow>
                ))}
                <TableRow>
                  <TableCell>Fixed Price Overall</TableCell>
                  <TableCell>
                    <Input
                      name="fixed_price_overall"
                      value={formData.fixed_price_overall}
                      onChange={handlePriceChange}
                      type="number"
                    />
                  </TableCell>
                  <TableCell>
                    <Input
                      name="net_fixed_price_overall"
                      value={formData.net_fixed_price_overall}
                      onChange={handlePriceChange}
                      type="number"
                    />
                  </TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Fixed Price Per Person</TableCell>
                  <TableCell>
                    <Input
                      name="fixed_price_per_person"
                      value={formData.fixed_price_per_person}
                      onChange={handlePriceChange}
                      type="number"
                    />
                  </TableCell>
                  <TableCell>
                    <Input
                      name="net_fixed_price_per_person"
                      value={formData.net_fixed_price_per_person}
                      onChange={handlePriceChange}
                      type="number"
                    />
                  </TableCell>
                </TableRow>
              </TableBody>
            </Table>
            <p className="text-sm italic text-gray-500">If net is empty, client becomes net</p>


          <div>
            <Label>Assign to Agents</Label>
            <MultiSelector 
              values={formData.agent_ids} 
              onValuesChange={handleAgentSelect}
            >
              <MultiSelectorTrigger>
                <MultiSelectorInput placeholder="Select agents" />
              </MultiSelectorTrigger>
              <MultiSelectorContent>
                <MultiSelectorList>
                  {agents?.map((agent) => (
                    <MultiSelectorItem key={agent.id} value={agent.id}>
                      {`${agent.first_name} ${agent.last_name}`}
                    </MultiSelectorItem>
                  ))}
                </MultiSelectorList>
              </MultiSelectorContent>
            </MultiSelector>
          </div>

          <div>
            <Label htmlFor="region_id">Assign to Region</Label>
            <SearchInput
              placeholder="Select a region..."
              searchPlaceholder="Search regions..."
              notFoundMessage="No region found."
              itemType="region"
              onItemSelect={handleRegionSelect}
              isLoading={false}
              data={regions}
              label={(region) => region.name}
              searchFields={['name']}
              idField="id"
              selectedValue={formData.region_id}
            />
          </div>


        </form>
      </CardContent>
      <CardFooter>
        <Button type="submit" onClick={handleSubmit} disabled={isAddingComponent}>
          {isAddingComponent ? 'Adding Component...' : 'Add Component'}
        </Button>
      </CardFooter>
    </Card>
    </div>
  );
}

