import React, { useState } from "react";
import { withStyles, makeStyles } from "@material-ui/core/styles";
import Menu from "@material-ui/core/Menu";
import MenuItem from "@material-ui/core/MenuItem";
import ListItemText from "@material-ui/core/ListItemText";
import IconButton from "@material-ui/core/IconButton";
import { useDispatch } from "react-redux";
import Typography from '@material-ui/core/Typography';
import {logUserOut} from '../../../../actions/userActions';

const useStyles = makeStyles((theme) => ({
  root: {
    "&:focus": {
      backgroundColor: theme.palette.primary.main,
      "& .MuiListItemIcon-root, & .MuiListItemText-primary": {
        color: theme.palette.common.white,
      },
    },
  },
  title: {
    flexGrow: 1,
  },
}));

const StyledMenu = withStyles({
  paper: {
    border: "1px solid #d3d4d5",
  },
})((props) => (
  <Menu 
    elevation={0}
    getContentAnchorEl={null}
    anchorOrigin={{
      vertical: "bottom",
      horizontal: "center",
    }}
    transformOrigin={{
      vertical: "top",
      horizontal: "center",
    }}
    {...props}
  />
));

const UserMenuDropDown = (props) => {
  const dispatch = useDispatch();
 
  const {user, ...rest} = props;

  const [anchorEl, setAnchorEl] = useState(null);
  const styles = useStyles();

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);

  };


  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <div>
      <IconButton
        {...rest}
        aria-controls="customized-menu"
        aria-haspopup="true"
        variant="contained"
        onClick={handleClick}
      >
        <Typography variant="h6" className={styles.title}> {user.first_name} {user.last_name}  </Typography>
      </IconButton>
      <StyledMenu
        id="customized-menu"
        anchorEl={anchorEl}
        keepMounted
        open={Boolean(anchorEl)}
        onClose={handleClose}
      >

        <MenuItem
          button
          className={styles.root}
          onClick={() => dispatch(logUserOut())}
        >
          <ListItemText primary='Log Out' />
        </MenuItem>


        <MenuItem
          button
          className={styles.root}
          onClick={() => dispatch(logUserOut())}
        >
          <ListItemText primary='Switch User' />
        </MenuItem>

        {/* CHANGE THE SWITCH USER TO A LIST OF USERS IN THE SAME ORGANIZATION, USING SIMILAR LOGIC TO BELOW  */}

        {/* {items.map((item) => (
          <MenuItem
            button
            key={`dropdown-${item.hotel_id}`}
            className={styles.root}
            onClick={() => dispatch(changeHotelView({ default_hotel: item.hotel_id }))}
          >
            <ListItemText primary={item.hotel_name} />
          </MenuItem>
        ))} */}


      </StyledMenu>
    </div>
  );
};



export default UserMenuDropDown;
