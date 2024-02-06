import React from "react";
import Grid from "@material-ui/core/Grid";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
  root: {
    marginTop: theme.spacing(0),
    marginRight: theme.spacing(0),
    marginLeft: theme.spacing(0),
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justify: "center",
    direction: "column",
  },
  formGrid: {
    maxWidth: "1200px",
    margin: "0 auto",
  },
  formColumn: {
    padding: theme.spacing(1),
  },
}));

const FormGrid = ({ children, ...props }) => {
  const styles = useStyles();

  return (
    <Grid
      container
      className={styles.root}
      component="main"
      {...props}
      spacing={1}
    >
      <Grid container className={styles.formGrid}>
        {children}
      </Grid>
    </Grid>
  );
};

export default FormGrid;