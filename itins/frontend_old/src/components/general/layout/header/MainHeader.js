import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import UserMenuDropDown from './UserMenuDropDown';
import { useSelector, useDispatch } from "react-redux";
import HotelMenuDropDown from "./HotelMenuDropDown";
import Grid from '@material-ui/core/Grid';
import items from '../../routes/RouteHelper.js'
import MenuIcon from '@material-ui/icons/Menu';
import MenuDropDownWithIcons from "../../MenuDropDownWithIcons";


// If you click switch user, it pops up with a dialog with all the users from that specif hotel/organisation and a bitton that says 'Not from this hotel?'

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  menuButton: {
    marginRight: theme.spacing(2),
  },
  title: {
    flexGrow: 1,
  },
}));


const MainHeader = () => {
  const classes = useStyles();
  const { user, loggedIn } = useSelector(state => state.userReducer);

  return (
    <div className={classes.root}>

      <AppBar position="static">
        <Toolbar>
          <Grid
            justify="space-between" // Add it here :)
            container 
          >
            {loggedIn &&
              <>
                <MenuDropDownWithIcons
                  items={items} 
                  menuIcon={<MenuIcon/>}
                  edge="start"
                  className={classes.menuButton}
                  color="inherit"
                  aria-label="open drawer"
                />
                <UserMenuDropDown
                  edge="start"
                  variant="h6"
                  color="inherit"
                  aria-label="open drawer"
                  user={user}
                />
                <HotelMenuDropDown
                  edge="start"
                  className={classes.menuButton}
                  color="inherit"
                  aria-label="open drawer"
                />
              </>
            }
          </Grid>
        </Toolbar>
      </AppBar>
    </div>
  );
}

export default MainHeader;