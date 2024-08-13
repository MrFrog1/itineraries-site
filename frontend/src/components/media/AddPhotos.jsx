import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { useToast } from "@/components/ui/use-toast";
import SearchInput from '../ui/SearchInput';
import { 
  useAddPhotoMutation, 
  useGetRegionsQuery, 
  useGetAllAgentsQuery, 
  useGetComponentsQuery,
  useGetItineraryGroupsQuery,
  useGetItineraryDaysQuery
} from '../../services/api';
import { useSelector } from 'react-redux';

export default function AddPhotos() {
  const hotels = useSelector(state => state.hotels.items);
  const agentItineraries = useSelector(state => state.itineraries.items);

  const [photos, setPhotos] = useState([]);
  const [selectedAgent, setSelectedAgent] = useState(null);

  const [addPhoto, { isLoading: isAddingPhoto }] = useAddPhotoMutation();
  const { data: regions, isLoading: isLoadingRegions } = useGetRegionsQuery();
  const { data: agents, isLoading: isLoadingAgents } = useGetAllAgentsQuery();
  const { data: components, isLoading: isLoadingComponents } = useGetComponentsQuery(selectedAgent, { skip: !selectedAgent });
  const { data: itineraryGroups, isLoading: isLoadingItineraryGroups } = useGetItineraryGroupsQuery(selectedAgent, { skip: !selectedAgent });
  const { data: itineraryDays, isLoading: isLoadingItineraryDays } = useGetItineraryDaysQuery(selectedAgent, { skip: !selectedAgent });

  const { toast } = useToast();

  const filteredHotels = selectedAgent ? hotels.filter(hotel => hotel.is_customized && hotel.hotel_owner === selectedAgent) : [];
  const filteredItineraries = selectedAgent ? agentItineraries.filter(itinerary => itinerary.agent === selectedAgent) : [];

  const onDrop = useCallback((acceptedFiles) => {
    setPhotos(prevPhotos => [
      ...prevPhotos,
      ...acceptedFiles.map(file => ({
        file,
        preview: URL.createObjectURL(file),
        tags: {
          uploader: selectedAgent,
          is_agent_bio_photo: false,
          primary_image: false,
          description: '',
          category: '',
          region: '',
          contact: null,
          review: null,
          hotel: null,
          hotel_activity: null,
          component: null,
          agent_itinerary: null,
          itinerary_group: null,
          itinerary_day: null,
        }
      }))
    ]);
  }, [selectedAgent]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ 
    onDrop,
    accept: {
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png']
    },
    maxSize: 5 * 1024 * 1024 // 5MB
  });

  const validatePhoto = (photo) => {
    const errors = {};
    if (!photo.tags.uploader) errors.uploader = "Uploader is required";
    return errors;
  };

  const handlePhotoUpload = async () => {
    for (let photo of photos) {
      const errors = validatePhoto(photo);
      if (Object.keys(errors).length > 0) {
        toast({
          title: "Validation Error",
          description: Object.values(errors).join(', '),
          status: "error"
        });
        return;
      }

      const formData = new FormData();
      formData.append('image', photo.file);
      Object.entries(photo.tags).forEach(([key, value]) => {
        if (value !== null && value !== '') {
          formData.append(key, value);
        }
      });

      try {
        await addPhoto(formData).unwrap();
        toast({
          title: "Photo uploaded",
          description: "The photo has been successfully uploaded.",
          status: "success"
        });
      } catch (error) {
        toast({
          title: "Upload failed",
          description: error.data?.detail || "Failed to upload photo. Please try again.",
          status: "error"
        });
      }
    }
    setPhotos([]);
  };

  const handleTagChange = (index, field, value) => {
    setPhotos(prevPhotos => {
      const newPhotos = [...prevPhotos];
      newPhotos[index].tags[field] = value;
      return newPhotos;
    });
  };

  const handleAgentSelect = (agent) => {
    setSelectedAgent(agent.id);
    setPhotos(prevPhotos => prevPhotos.map(photo => ({
      ...photo,
      tags: { 
        ...photo.tags, 
        uploader: agent.id,
        component: null,
        agent_itinerary: null,
        itinerary_group: null,
        itinerary_day: null
      }
    })));
  };

  return (
    <Card className="w-full max-w-4xl">
      <CardHeader>
        <CardTitle>Add Photos</CardTitle>
        <CardDescription>Upload and tag photos for the platform.</CardDescription>
      </CardHeader>
      <CardContent>
        <div {...getRootProps()} className={`border-2 border-dashed rounded-md p-4 ${isDragActive ? 'border-primary' : 'border-muted'}`}>
          <input {...getInputProps()} />
          <p>{isDragActive ? "Drop the files here ..." : "Drag 'n' drop some files here, or click to select files"}</p>
        </div>
        <div className="mt-4">
          <Label htmlFor="agent">Uploader (Agent)</Label>
          <SearchInput
            id="agent"
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
            selectedValue={selectedAgent}
          />
        </div>
        {photos.map((photo, index) => (
          <div key={index} className="mt-4 p-4 border rounded">
            <img src={photo.preview} alt={`Preview ${index}`} className="w-32 h-32 object-cover mb-4" />
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor={`description-${index}`}>Description</Label>
                <Input 
                  id={`description-${index}`}
                  value={photo.tags.description}
                  onChange={(e) => handleTagChange(index, 'description', e.target.value)} 
                />
              </div>
              <div>
                <Label htmlFor={`category-${index}`}>Category</Label>
                <Input 
                  id={`category-${index}`}
                  value={photo.tags.category}
                  onChange={(e) => handleTagChange(index, 'category', e.target.value)} 
                />
              </div>
              <div>
                <Label htmlFor={`region-${index}`}>Region</Label>
                <SearchInput
                  id={`region-${index}`}
                  placeholder="Select region..."
                  searchPlaceholder="Search regions..."
                  notFoundMessage="No region found."
                  itemType="region"
                  onItemSelect={(region) => handleTagChange(index, 'region', region.id)}
                  isLoading={isLoadingRegions}
                  data={regions}
                  label={(region) => region.name}
                  searchFields={['name']}
                  idField="id"
                  selectedValue={photo.tags.region}
                />
              </div>
              <div>
                <Label htmlFor={`hotel-${index}`}>Hotel</Label>
              <SearchInput
                id={`hotel-${index}`}
                placeholder="Select hotel..."
                searchPlaceholder="Search hotels..."
                notFoundMessage="No hotel found."
                itemType="hotel"
                onItemSelect={(hotel) => handleTagChange(index, 'hotel', hotel.id)}
                isLoading={false}
                data={filteredHotels}
                label={(hotel) => `${hotel.name}`}
                searchFields={['name']}
                idField="id"
                selectedValue={photo.tags.hotel}
              />
              </div>
              <div>
                <Label htmlFor={`component-${index}`}>Component</Label>
                {selectedAgent ? (
                  <SearchInput
                    id={`component-${index}`}
                    placeholder="Select component..."
                    searchPlaceholder="Search components..."
                    notFoundMessage="No component found."
                    itemType="component"
                    onItemSelect={(component) => handleTagChange(index, 'component', component.id)}
                    isLoading={isLoadingComponents}
                    data={components || []}
                    label={(component) => component.name}
                    searchFields={['name']}
                    idField="id"
                    selectedValue={photo.tags.component}
                    disabled={!selectedAgent}
                  />
                ) : (
                  <p className="text-sm text-gray-500">Please select an agent to view components.</p>
                )}
              </div>
              <div>
                <Label htmlFor={`agent_itinerary-${index}`}>Agent Itinerary</Label>
              <SearchInput
                id={`agent_itinerary-${index}`}
                placeholder="Select agent itinerary..."
                searchPlaceholder="Search agent itineraries..."
                notFoundMessage="No agent itinerary found."
                itemType="agent_itinerary"
                onItemSelect={(itinerary) => handleTagChange(index, 'agent_itinerary', itinerary.id)}
                isLoading={false}
                data={filteredItineraries}
                label={(itinerary) => itinerary.name}
                searchFields={['name']}
                idField="id"
                selectedValue={photo.tags.agent_itinerary}
                disabled={!selectedAgent}
              />
              </div>
              <div>
                <Label htmlFor={`itinerary_group-${index}`}>Itinerary Group</Label>
                <SearchInput
                  id={`itinerary_group-${index}`}
                  placeholder="Select itinerary group..."
                  searchPlaceholder="Search itinerary groups..."
                  notFoundMessage="No itinerary group found."
                  itemType="itinerary_group"
                  onItemSelect={(group) => handleTagChange(index, 'itinerary_group', group.id)}
                  isLoading={isLoadingItineraryGroups}
                  data={itineraryGroups || []}
                  label={(group) => group.name}
                  searchFields={['name']}
                  idField="id"
                  selectedValue={photo.tags.itinerary_group}
                  disabled={!selectedAgent}
                />
              </div>
              <div>
                <Label htmlFor={`itinerary_day-${index}`}>Itinerary Day</Label>
                <SearchInput
                  id={`itinerary_day-${index}`}
                  placeholder="Select itinerary day..."
                  searchPlaceholder="Search itinerary days..."
                  notFoundMessage="No itinerary day found."
                  itemType="itinerary_day"
                  onItemSelect={(day) => handleTagChange(index, 'itinerary_day', day.id)}
                  isLoading={isLoadingItineraryDays}
                  data={itineraryDays || []}
                  label={(day) => day.name}
                  searchFields={['name']}
                  idField="id"
                  selectedValue={photo.tags.itinerary_day}
                  disabled={!selectedAgent}
                />
              </div>
              <div className="col-span-2">
                <div className="flex items-center space-x-2">
                  <Switch 
                    id={`is_agent_bio_photo-${index}`}
                    checked={photo.tags.is_agent_bio_photo}
                    onCheckedChange={(checked) => handleTagChange(index, 'is_agent_bio_photo', checked)}
                  />
                  <Label htmlFor={`is_agent_bio_photo-${index}`}>Agent Bio Photo</Label>
                </div>
              </div>
              <div className="col-span-2">
                <div className="flex items-center space-x-2">
                  <Switch 
                    id={`primary_image-${index}`}
                    checked={photo.tags.primary_image}
                    onCheckedChange={(checked) => handleTagChange(index, 'primary_image', checked)}
                  />
                  <Label htmlFor={`primary_image-${index}`}>Primary Image</Label>
                </div>
              </div>
            </div>
          </div>
        ))}
      </CardContent>
      <CardFooter>
        <Button onClick={handlePhotoUpload} disabled={isAddingPhoto || photos.length === 0}>
          {isAddingPhoto ? 'Uploading Photos...' : 'Upload Photos'}
        </Button>
      </CardFooter>
    </Card>
  );
}