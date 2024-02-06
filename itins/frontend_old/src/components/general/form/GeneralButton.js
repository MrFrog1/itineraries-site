import React from "react";
import Button from "@material-ui/core/Button";
import { makeStyles } from "@material-ui/core/styles";

// Note - this is only meant for user when integrated with React Hook Forms.
// For a more general use Button, go to features

const useStyles = makeStyles((theme) => ({
  root: {
    margin: theme.spacing(3, 0, 2),
  },
}));

const GeneralButton = ({ children, ...props }) => {
  const styles = useStyles();

  return (
    <Button
      type="button"
      variant="contained"
      color="primary"
      className={styles.root}
      {...props}
    >
      {children}
    </Button>
  );
};

export default GeneralButton;
