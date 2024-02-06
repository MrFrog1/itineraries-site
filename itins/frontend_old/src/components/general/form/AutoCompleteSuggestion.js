import React, { useState, useEffect } from "react";
import Autocomplete, { createFilterOptions } from "@material-ui/lab/Autocomplete";
import parse from "autosuggest-highlight/parse";
import match from "autosuggest-highlight/match";
import { Controller } from "react-hook-form";
import Button from "@material-ui/core/Button";
import Input from './Input'
  

const AutoCompleteSuggestion = (props) => {
  
  const [texts, setTexts] = useState('');
  const [heldInfo, setHeldInfo] = useState('');

  useEffect(() => {    
    // console.log(props.heldData)
    if (props.heldData){
      if (props.heldData[props.name]) {
        setHeldInfo(props.items.find(o=> o[props.selection] === props.heldData[props.name])[props.label1]);
      }
    }

  },[])

  const handleInputChange = (e) => {
    setTexts(e.target.value)
    setHeldInfo('')
  }

  return (
    <>
      <Controller
        name={props.name}
        control={props.control}
        // defaultValue={value}
        render={({ onChange }) => (
          <Autocomplete
            id={props.implementation}
            style={{ width: 320 }}
            options={props.items}
            inputValue={heldInfo? heldInfo:texts}
            debug={true}
            getOptionLabel={(option) => option[props.label1]}
            noOptionsText = {<Button onClick={()=> props.openSecondComponent(props.name, texts)}>Add {texts} as a {props.implementation}</Button>}
            onChange={(e, data) => {
              if (data==null){
                onChange(null)
              } else {
                console.log(data)
                setTexts(data[props.label1]);
                onChange(data[props.selection]);
                // HERE, WE MANAGE TO CHANGE HE ACTUAL DATA TO THE SELECTION (ID), BUT WE TRY TO CHANGE THE INPUT VALUE AND IT DOESNT WORK

              }
            }} //this passes upwards to the onChange in Controller. Needs the e for the event
            renderInput={(params) => (
              <Input
                {...params}
                label={props.implementation}
                error={props.error}
                helperText={props.helperText}
                onChange = {handleInputChange}
              /> 
            )}
            renderOption={(option, { inputValue }) => {
              const matches = match(option[props.label1], inputValue);
              const parts = parse(option[props.label1], matches);

              return (
                <div>
                  {option[props.label2]} -
                  {parts.map((part, index) => (
                    <span
                      key={index}
                      style={{ fontWeight: part.highlight ? 700 : 400 }}
                    >
                      {part.text}
                    </span>
                  ))}
                </div>
              );
            }}
          />
        )}
      />
    </>
  );
};

export default AutoCompleteSuggestion;
