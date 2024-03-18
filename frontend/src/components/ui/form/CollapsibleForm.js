import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Switch from '@material-ui/core/Switch';
import Collapse from '@material-ui/core/Collapse';
import FormControlLabel from '@material-ui/core/FormControlLabel';

const useStyles = makeStyles((theme) => ({
  root: {
  },
  container: {
    display: 'flex',
  },

}));

const CollapsibleForm = ({children, ...props}) => {
  const styles = useStyles();
  const [checked, setChecked] = React.useState(false);

  const handleChange = () => {
    setChecked((prev) => !prev);
  };

  return (
    <div className={styles.root}>
      <FormControlLabel
        control={<Switch checked={checked} onChange={handleChange} />}
        {...props}      />
      <div className={styles.container}>
        <Collapse in={checked}>
            {
                children
            }
        </Collapse>
      </div>
    </div>
  );
}

export default CollapsibleForm;