import React, { useState, useEffect } from "react";
import { CheckIcon } from './icons'
import { CaretSortIcon } from "@radix-ui/react-icons";
import { cn } from "@/lib/utils";
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

export default function SearchInput({ 
  data, 
  onItemSelect, // Changed from onSelect to onItemSelect
  onSearch, // Added this prop
  placeholder = "Select item...",
  label = (item) => item.name,
  searchFields = ['name'],
  idField = 'id',
  isLoading = false
}) {
  const [open, setOpen] = useState(false);
  const [value, setValue] = useState("");
  const [filteredData, setFilteredData] = useState([]);

  useEffect(() => {
    if (data) {
      setFilteredData(data);
    }
  }, [data]);

  const handleSearch = (searchTerm) => {
    if (!data) return;
    const filtered = data.filter((item) =>
      searchFields.some(field => 
        String(item[field]).toLowerCase().includes(searchTerm.toLowerCase())
      )
    );
    setFilteredData(filtered);
    onSearch(searchTerm); // Call the passed onSearch function
  };

  return (
    <div>
      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger asChild>
          <Button
            variant="outline"
            role="combobox"
            aria-expanded={open}
            className="w-full justify-between"
          >
            {value
              ? label(data?.find((item) => String(item[idField]) === value))
              : placeholder}
            <CaretSortIcon className="ml-2 h-4 w-4 shrink-0 opacity-50" />
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-[300px] p-0">
          <Command>
            <CommandInput placeholder={`Search ${placeholder.toLowerCase()}...`} onValueChange={handleSearch} />
            {isLoading ? (
              <CommandItem>Loading...</CommandItem>
            ) : (
              <>
                {filteredData.length === 0 && <CommandEmpty>No item found.</CommandEmpty>}
                {filteredData.length > 0 && (
                  <CommandGroup>
                    <CommandList>
                      {filteredData.map((item) => (
                        <CommandItem
                          key={item[idField]}
                          value={String(item[idField])}
                          onSelect={(currentValue) => {
                            setValue(currentValue);
                            setOpen(false);
                            onItemSelect(data.find(i => String(i[idField]) === currentValue)); // Changed from onSelect to onItemSelect
                          }}
                        >
                          <CheckIcon
                            className={cn(
                              "mr-2 h-4 w-4",
                              value === String(item[idField]) ? "opacity-100" : "opacity-0"
                            )}
                          />
                          {label(item)}
                        </CommandItem>
                      ))}
                    </CommandList>
                  </CommandGroup>
                )}
              </>
            )}
          </Command>
        </PopoverContent>
      </Popover>
    </div>
  );
}


// Working with localised data

// import React, { useState, useEffect } from "react";
// import { CheckIcon } from './icons'
// import { CaretSortIcon } from "@radix-ui/react-icons";
// import { cn } from "@/lib/utils";
// import { Button } from "@/components/ui/button";
// import {
//   Command,
//   CommandEmpty,
//   CommandGroup,
//   CommandInput,
//   CommandItem,
//   CommandList,
// } from "@/components/ui/command";
// import {
//   Popover,
//   PopoverContent,
//   PopoverTrigger,
// } from "@/components/ui/popover";

// export default function SearchInput({ 
//   data, 
//   onSelect, 
//   placeholder = "Select item...",
//   label = (item) => item.name,
//   searchFields = ['name'],
//   idField = 'id'
// }) {
//   const [open, setOpen] = useState(false);
//   const [value, setValue] = useState("");
//   const [filteredData, setFilteredData] = useState(data);

//   useEffect(() => {
//     setFilteredData(data);
//   }, [data]);

//   const handleSearch = (searchTerm) => {
//     const filtered = data.filter((item) =>
//       searchFields.some(field => 
//         String(item[field]).toLowerCase().includes(searchTerm.toLowerCase())
//       )
//     );
//     setFilteredData(filtered);
//   };

//   return (
//     <div>
//       <Popover open={open} onOpenChange={setOpen}>
//         <PopoverTrigger asChild>
//           <Button
//             variant="outline"
//             role="combobox"
//             aria-expanded={open}
//             className="w-full justify-between"
//           >
//             {value
//               ? label(data.find((item) => String(item[idField]) === value))
//               : placeholder}
//             <CaretSortIcon className="ml-2 h-4 w-4 shrink-0 opacity-50" />
//           </Button>
//         </PopoverTrigger>
//         <PopoverContent className="w-[300px] p-0">
//           <Command>
//             <CommandInput placeholder={`Search ${placeholder.toLowerCase()}...`} onValueChange={handleSearch} />
//             <CommandEmpty>No item found.</CommandEmpty>
//             <CommandGroup>
//               <CommandList>
//                 {filteredData.map((item) => (
//                   <CommandItem
//                     key={item[idField]}
//                     value={String(item[idField])}
//                     onSelect={(currentValue) => {
//                       setValue(currentValue);
//                       setOpen(false);
//                       onSelect(data.find(i => String(i[idField]) === currentValue));
//                     }}
//                   >
//                     <CheckIcon
//                       className={cn(
//                         "mr-2 h-4 w-4",
//                         value === String(item[idField]) ? "opacity-100" : "opacity-0"
//                       )}
//                     />
//                     {label(item)}
//                   </CommandItem>
//                 ))}
//               </CommandList>
//             </CommandGroup>
//           </Command>
//         </PopoverContent>
//       </Popover>
//     </div>
//   );
// }



// import React, { useState, useEffect } from 'react';
// import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "@/components/ui/command";
// import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";

// export default function SearchInput({
//   placeholder,
//   onSearch,
//   isLoading,
//   items,
//   onItemSelect,
//   renderItem,
//   addNewComponent: AddNewComponent,
//   addNewButtonText,
//   dialogTitle,
//   dialogDescription,
//   minSearchLength = 2
// }) {
//   const [searchTerm, setSearchTerm] = useState('');
//   const [showAddNew, setShowAddNew] = useState(false);
//   const [open, setOpen] = useState(false);

//   useEffect(() => {
//     console.log('SearchInput - Items:', items);
//     console.log('SearchInput - Is Loading:', isLoading);
//   }, [items, isLoading]);

//   useEffect(() => {
//     if (searchTerm.length >= minSearchLength) {
//       setOpen(true);
//       onSearch(searchTerm);
//     } else {
//       setOpen(false);
//     }
//   }, [searchTerm, minSearchLength, onSearch]);

//   const handleSearch = (value) => {
//     console.log('SearchInput - Search term:', value);
//     setSearchTerm(value);
//   };

//   const handleSelectItem = (item) => {
//     onItemSelect(item);
//     setSearchTerm('');
//     setOpen(false);
//   };

//   const safeItems = Array.isArray(items) ? items : [];

//   // const handleAddNewItem = (newItem) => {
//   //   onItemSelect(newItem);
//   //   setShowAddNew(false);
//   //   setSearchTerm('');
//   //   setOpen(false);
//   // };

//   // console.log('Items in SearchInput:', items);
//   // console.log('Is Loading in SearchInput:', isLoading);

//  return (
//     <>
//       <Command className="rounded-lg border shadow-md">
//         <CommandInput 
//           placeholder={placeholder}
//           value={searchTerm}
//           onValueChange={handleSearch}
//         />
//         {open && (
//           <CommandList>
//             {isLoading && <CommandItem>Loading...</CommandItem>}
//             {!isLoading && safeItems.length === 0 && <CommandEmpty>No results found.</CommandEmpty>}
//             {!isLoading && safeItems.length > 0 && (
//               <CommandGroup heading="Suggestions">
//                 {safeItems.map((item) => (
//                   <CommandItem 
//                     key={item.id} 
//                     onSelect={() => handleSelectItem(item)}
//                   >
//                     {renderItem(item)}
//                   </CommandItem>
//                 ))}
//               </CommandGroup>
//             )}
//             {searchTerm.length >= minSearchLength && AddNewComponent && (
//               <CommandItem onSelect={() => setShowAddNew(true)}>
//                 {addNewButtonText}: {searchTerm}
//               </CommandItem>
//             )}
//           </CommandList>
//         )}
//       </Command>
      
//       {showAddNew && (
//         <Dialog open={showAddNew} onOpenChange={setShowAddNew}>
//           <DialogContent>
//             <DialogHeader>
//               <DialogTitle>{dialogTitle}</DialogTitle>
//               <DialogDescription>{dialogDescription}</DialogDescription>
//             </DialogHeader>
//             <AddNewComponent initialName={searchTerm} onItemAdded={handleAddNewItem} />
//           </DialogContent>
//         </Dialog>
//       )}
//     </>
//   );
// }