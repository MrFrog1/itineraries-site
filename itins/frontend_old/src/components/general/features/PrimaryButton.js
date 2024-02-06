import React from "react";
import Button from "@material-ui/core/Button";
import { makeStyles } from "@material-ui/core/styles";

// Note - this is only meant for user when integrated with React Hook Forms.
// For a more general use Button, go to features

const useStyles = makeStyles(theme => ({
    root: {
        minWidth: 0,
        margin: theme.spacing(0.5)
    },
    secondary: {
        backgroundColor: theme.palette.secondary.light,
        '& .MuiButton-label': {
            color: theme.palette.secondary.main,
        }
    },
    primary: {
        backgroundColor: theme.palette.primary.light,
        '& .MuiButton-label': {
            color: theme.palette.primary.main,
        }
    },
}))

const PrimaryButton = ({ children, color, onClick }) => {
  const styles = useStyles();

  return (
    <Button
      className={`${styles.root} ${styles[color]}`}
      onClick={onClick}
    >
      {children}
    </Button>
  );
};

export default PrimaryButton;
