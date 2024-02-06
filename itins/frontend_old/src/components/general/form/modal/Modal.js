import React from "react";
import Dialog from '@material-ui/core/Dialog';
import DialogTitle from '@material-ui/core/DialogTitle';
import DialogContent from '@material-ui/core/DialogContent';
import { makeStyles } from "@material-ui/core/styles";
import Typography from '@material-ui/core/Typography'
import CloseIcon from "@material-ui/icons/Close";
import PrimaryButton from "../../features/PrimaryButton.js";

const useStyles = makeStyles((theme) => ({
  dialogWrapper: {
    padding: theme.spacing(2),
    position: "absolute",
    top: theme.spacing(5),
    
  },
  dialogTitle: {
    paddingRight: "0px",
  },
  modalContent: {
    minWidth: '50%', // Set a custom width, for example, 50% of the parent container.
    [theme.breakpoints.down('sm')]: {
      minWidth: '100%', // Set the width to 100% for small screens.
    },
  },
}));

export default function Modal(props) {
  const { title, children, openModal, setOpenModal } = props;
  const styles = useStyles();

  return (
    <Dialog
      open={openModal}
      onBackdropClick={() => {setOpenModal(false)}}
      fullWidth
      classes={{ paper: styles.dialogWrapper }}
    >
      <DialogTitle className={styles.dialogTitle}>
        <div style={{ display: "flex" }}>
          <Typography align="left" variant="h5" component="div" style={{ flexGrow: 1 }}>
            {title}
          </Typography>
          <PrimaryButton
            color="primary"
            onClick={() => {
              setOpenModal(false);
            }}
          >
            <CloseIcon />
          </PrimaryButton>
        </div>
      </DialogTitle>
      <DialogContent dividers className={styles.modalContent}>{children}</DialogContent>
    </Dialog>
  );
}
