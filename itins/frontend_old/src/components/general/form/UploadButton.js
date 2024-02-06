import React, { useEffect, forwardRef } from "react";
import Button from "@material-ui/core/Button";
import { makeStyles } from "@material-ui/core/styles";

// Note - this is only meant for user when integrated with React Hook Forms.
// For a more general use Button, go to features

const useStyles = makeStyles((theme) => ({
  root: {
    '& > *': {
      margin: theme.spacing(1),
    },
  },
  input: {
    display: 'none',
  },
}));


// Props only in the input. Children inside the button 


const UploadButton = ({children,...props}) => {
  const styles = useStyles();

  const {startIcon,...rest} = props;

  useEffect(() => {
    console.log(props.id)
    // console.log(props.id)
  })
  return (
    <div className={styles.root}>
      <input className={styles.input} {...rest}/>
      <label htmlFor={props.id}>
        <Button variant="contained" startIcon={startIcon} color="primary" component="span">
          {children}
        </Button>
      </label>
    </div>

  );
};

export default UploadButton;
