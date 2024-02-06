import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Collapse from '@material-ui/core/Collapse';

const useStyles = makeStyles((theme) => ({
  root: {
  },
  container: {
    display: 'flex',
  },

}));

const CollapsibleBasic = ({children, watcher, ...props}) => {
  const styles = useStyles();
  
  const watcher2 = watcher===''? false: true

  return (
    <div className={styles.root}>
      <div className={styles.container}>
        <Collapse in={watcher2}>
            {
                children
            }
        </Collapse>
      </div>
    </div>
  );
}

export default CollapsibleBasic;