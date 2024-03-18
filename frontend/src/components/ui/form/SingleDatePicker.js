import DateFnsUtils from "@date-io/date-fns";
import {
  MuiPickersUtilsProvider,
  KeyboardDatePicker,
} from "@material-ui/pickers";
import React from 'react';
import { Controller } from "react-hook-form";


const SingleDatePicker = ({label,id,name,control,maxDate,focusDate}) => {

  return (
        <MuiPickersUtilsProvider utils={DateFnsUtils}>
          <Controller
            name={name}
            defaultValue={null}
            control={control}
            render={({ref,...rest}) => (
              <KeyboardDatePicker
                margin="normal"
                format="dd/MM/yyyy"
                initialFocusedDate= {focusDate}
                KeyboardButtonProps={{
                  "aria-label": "change date"
                }}
                InputLabelProps={{ shrink: true }}
                {...rest}
                id ={id}
                label={label}
                emptyLabel=''
                maxDate= {maxDate}
                onBlur={rest.onBlur}
                onChange={(value) => {rest.onChange(value)}}

              />
            )}
          />
        </MuiPickersUtilsProvider>
        
    )
}

export default SingleDatePicker;

