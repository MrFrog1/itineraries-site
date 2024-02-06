import FormControl from "@material-ui/core/FormControl";
import InputLabel from "@material-ui/core/InputLabel";
import Select from "@material-ui/core/Select";
import { Controller } from "react-hook-form";
import React from "react";
import { makeStyles } from '@material-ui/core/styles';
import FormHelperText from '@material-ui/core/FormHelperText';

const style = {
  color: 'red',
};

const useStyles = makeStyles((theme) => ({
  formControl: {
    marginTop: theme.spacing(2),
  },
  error: {
    color: 'red',
  }
}));


const DropDownSelect = ({
  name,
  label,
  control,
  defaultValue,
  children,
  error,
  helperText,
  ...rest
}) => {
  const styles= useStyles();
  const labelId = `${name}-label`;
  return (
    <FormControl variant="outlined" {...rest} className={styles.formControl}>
      <InputLabel id={labelId}>{label}</InputLabel>
      <Controller
        name={name}
        control={control}
        defaultValue={defaultValue}

        render={(props)=> (
          <>
            <Select labelId={labelId} error={error} label={label} {...props}>
              {children}
            </Select>
            <FormHelperText style={style}>
              {helperText}
            </FormHelperText>
          </>

        )}
      />
    </FormControl>
  );
};
export default DropDownSelect;


      // <FormControl variant="outlined" className={classes.formControl}>
      //   <InputLabel id="demo-simple-select-outlined-label">Age</InputLabel>
      //   <Select
      //     labelId="demo-simple-select-outlined-label"
      //     id="demo-simple-select-outlined"
      //     value={age}
      //     onChange={handleChange}
      //     label="Age"
      //   >
      //     <MenuItem value="">
      //       <em>None</em>
      //     </MenuItem>
      //     <MenuItem value={10}>Ten</MenuItem>
      //     <MenuItem value={20}>Twenty</MenuItem>
      //     <MenuItem value={320}>d</MenuItem>
      //   </Select>
      // </FormControl>