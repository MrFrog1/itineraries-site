import React, { useState } from 'react';
import { useAddComponentTypeMutation, useGetAllAgentsQuery } from '../../services/api';
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { useToast } from "@/components/ui/use-toast";
import SearchInput from '../ui/SearchInput';

export default function AddComponentTypeForm({ onComponentTypeAdded, onAgentChange }) {
  const [name, setName] = useState('');
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [addComponentType, { isLoading }] = useAddComponentTypeMutation();
  const { data: agents, isLoading: isLoadingAgents } = useGetAllAgentsQuery();
  const { toast } = useToast();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const componentTypeData = {
        name,
        agent: selectedAgent ? selectedAgent.id : undefined,
        is_global: false // Ensure new types created here are not global
      };
      
      const result = await addComponentType(componentTypeData).unwrap();
      toast({
        title: "Component Type Added",
        description: "The new component type has been successfully added.",
        status: "success"
      });
      setName('');
      
      if (onComponentTypeAdded) {
        onComponentTypeAdded(result);
      }
    } catch (error) {
      toast({
        title: "Error",
        description: error.data?.detail || "Failed to add component type. Please try again.",
        status: "error"
      });
    }
  };

  const handleAgentSelect = (agent) => {
    setSelectedAgent(agent);
    if (onAgentChange) {
      onAgentChange(agent);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <Label htmlFor="componentTypeName">Component Type Name</Label>
        <Input
          id="componentTypeName"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
      </div>
      <div>
        <Label htmlFor="agent">Agent</Label>
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
          selectedValue={selectedAgent ? selectedAgent.id : null}
          required
        />
      </div>
      <Button type="submit" disabled={isLoading || !selectedAgent}> 
        {isLoading ? 'Adding...' : 'Add Component Type'}
      </Button>
    </form>
  );
}