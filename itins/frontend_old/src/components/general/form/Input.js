import { TextField } from '@material-ui/core';
import React, { forwardRef } from 'react';

// Note - this is only meant for user when integrated with React Hook Forms.
// For a more general use InPut, go to features


export const Input = forwardRef((props,ref) =>{
    return (<TextField 
        variant="outlined" 
        margin="normal" 
        inputRef ={ref} 
        {...props}/> 
    );
});

export default Input; 