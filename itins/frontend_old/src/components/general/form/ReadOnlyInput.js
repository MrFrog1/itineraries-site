import { TextField } from "@material-ui/core";
import React from "react";


export const ReadOnlyInput = (props) => {
  return (
    <TextField
      variant="outlined"
      margin="normal"
      InputProps={{
        readOnly: true,
      }}
      {...props}
    />
  );
};

export default ReadOnlyInput;
