import React from 'react'
import { connect } from 'react-redux';
import { Link, Route, useParams, useRouteMatch } from 'react-router-dom';


// this const Item is completely variable as to where you go with it. So, 
// if you go to settings/strange it will return strange from the userparams and then print that out in the h3
// example from here: https://www.sitepoint.com/react-router-complete-guide/
// /currently not working but should, when you click on account, payment etc, come up with Account, Payment etc. 

const Item = () => { 
  const { name } = useParams();

  return (
    <div>
      <h3>{name}</h3>
    </div>
  );
}

const Settings = () => {
  const { url, path } = useRouteMatch();

  return (
    <div>
      <ul>
        <li>
          <Link to={`${url}/payment`}>Payment Settings</Link>
        </li>
        <li>
          <Link to={`${url}/account`}>Account Settings</Link>
        </li>
        <li>
          <Link to={`${url}/terms_and_conditions`}>Terms and Conditions</Link>
        </li>
      </ul>
      <Route path={`${path}/:name`}>
        <Item />
      </Route>
    </div>
  );
};

export default Settings;