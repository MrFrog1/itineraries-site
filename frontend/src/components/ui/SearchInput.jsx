import React, { useState, useMemo, useEffect } from 'react';
import { Check, ChevronsUpDown } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import {
  Popover, 
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { cn } from "@/lib/utils";

export default function SearchInput({ 
  data = [],
  onItemSelect,
  placeholder = "Select...",
  searchPlaceholder = "Search...",
  notFoundMessage = "No item found.",
  itemType = "item", // New prop for the type of item being searched
  idField = 'id',
  searchFields = ['name'],
  isLoading = false,
  selectedValue = null,
  label  // Function to generate label for an item
}) {
  const [open, setOpen] = useState(false);
  const [value, setValue] = useState(selectedValue);
  const [searchTerm, setSearchTerm] = useState("");


  // Update local value when selectedValue prop changes
  useEffect(() => {
    setValue(selectedValue);
  }, [selectedValue]);

  const filteredData = useMemo(() => {
    if (!data || !Array.isArray(data) || data.length === 0) return [];
    return data.filter((item) =>
      searchFields.some(field => {
        const fieldValue = item[field];
        return fieldValue && String(fieldValue).toLowerCase().includes(searchTerm.toLowerCase());
      })
    );
  }, [data, searchFields, searchTerm]);

  const handleSearch = (term) => {
    setSearchTerm(term);
    if (!open) setOpen(true);
  };

  const selectedItem = data.find((item) => String(item[idField]) === String(value));

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          aria-expanded={open}
          className="w-full justify-between"
        >
          {selectedItem 
            ? label(selectedItem)
            : placeholder}
          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[500px] p-0">
        <Command>
          <CommandInput 
            placeholder={searchPlaceholder}
            value={searchTerm}
            onValueChange={handleSearch}
          />
          <CommandList>
            {isLoading ? (
              <CommandItem>Loading...</CommandItem>
            ) : (
              <>
                {filteredData.length === 0 ? (
                  <CommandEmpty>{notFoundMessage}</CommandEmpty>
                ) : (
                  <CommandGroup>
                    {filteredData.map((item) => (
                      <CommandItem
                        key={item[idField]}
                        value={item[idField]}
                        onSelect={(currentValue) => {
                          setValue(currentValue);
                          setOpen(false);
                          onItemSelect(item);
                        }}
                      >
                        <Check
                          className={cn(
                            "mr-2 h-4 w-4",
                            value === item[idField] ? "opacity-100" : "opacity-0"
                          )}
                        />
                        {label(item)}
                      </CommandItem>
                    ))}
                  </CommandGroup>
                )}
              </>
            )}
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  );
}