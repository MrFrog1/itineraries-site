import React, { forwardRef } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';

const useStyles = makeStyles((theme) => ({

  textField: {
    marginLeft: theme.spacing(1),
    marginRight: theme.spacing(1),
    width: 200,
  },
}));

const TimePicker= forwardRef((props,ref) => {

  const classes = useStyles();

  return (
      <TextField
        {...props}
        type="time"
        inputRef={ref}
        className={classes.textField}
        InputLabelProps={{
          shrink: true,
        }}
        inputProps={{
          step: 300, // 5 min
        }}
      />
  );
})

export default TimePicker;