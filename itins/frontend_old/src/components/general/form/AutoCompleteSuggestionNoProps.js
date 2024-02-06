/* eslint-disable no-use-before-define */
import React, { Fragment, useEffect, useState } from "react";
import axios from "axios";
import axiosInstance from "../general_functions/Axios";
import TextField from "@material-ui/core/TextField";
import Autocomplete from "@material-ui/lab/Autocomplete";
import parse from "autosuggest-highlight/parse";
import match from "autosuggest-highlight/match";
import { Controller } from "react-hook-form";

// After, turn into arrow fuinction and use dispatch for errors.

const AutoCompleteSuggestion = (props) => {
  const [items, setItems] = useState([]);


  const fetchItems = () => {
    axios
      .get(props.url, config)
      .then((res) => {
        const items = res.data;
        setItems(items);
      })
      .catch((err) => console.log(err)); //in case there is an error. Can have an error reducer that sends errors down to our components.
  };

  useEffect(() => {
    fetchItems();
  }, []);

  return (
    <Controller
      name={props.name}
      control={props.control}
      defaultValue={null}
      onChange={([, data]) => data}
      render={({ onChange }) => (
        <Autocomplete
          id={props.implementation}
          style={{ width: 300 }}
          options={items}
          getOptionLabel={(option) => option[props.label1]}
          onChange={(e, data) => onChange(data)} //this passes upwards to the onChange in Controller. Needs the e for the event
          renderInput={(params) => (
            <TextField
              {...params}
              label={props.implementation}
              variant="outlined"
              margin="normal"
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
  );
};

export default AutoCompleteSuggestion;
