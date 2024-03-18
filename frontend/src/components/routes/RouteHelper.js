import React from 'react';
import TodayIcon from '@material-ui/icons/Today';
import PeopleAltIcon from '@material-ui/icons/PeopleAlt';
import PaymentIcon from '@material-ui/icons/Payment';
import ImportExportIcon from '@material-ui/icons/ImportExport';
import AssignmentIcon from '@material-ui/icons/Assignment';
import EmojiTransportationIcon from '@material-ui/icons/EmojiTransportation';
import SettingsIcon from '@material-ui/icons/Settings';
import RecordVoiceOverTwoToneIcon from '@material-ui/icons/RecordVoiceOverTwoTone';

const items = {
  'Calendar': {component: (<TodayIcon fontSize="small"/>), pageComponent: (<TodayIcon fontSize="large"/>), link:'/calendar', header: 'Bookings Calendar', subHeader:''},
  'Bookings and Guests':   {component: (<PeopleAltIcon fontSize="small"/>) , pageComponent: (<PeopleAltIcon fontSize="large"/>), link: '/bookings', header: 'Booking and Guest Management', subHeader:''},
  'Dashboard':   {component: (<PeopleAltIcon fontSize="small"/>) , pageComponent: (<PeopleAltIcon fontSize="large"/>), link: '/bookings', header: 'Dashboard', subHeader:"Your central control of your hotel's operations"},
  'Bills': {component: (<PaymentIcon fontSize="small"/>), pageComponent: (<PaymentIcon fontSize="large"/>), link: '/bills', header: 'Bills and POS', subHeader:''},
  'Accounts': {component: (<ImportExportIcon fontSize="small"/>), pageComponent: (<ImportExportIcon fontSize="large"/>), link: '/accounts', header: 'Accounts', subHeader:'Manage Incoming and Outgoing'},
  'Tasks and Rota': {component: (<AssignmentIcon fontSize="small"/>), pageComponent: (<AssignmentIcon fontSize="large"/>), link: '/tasks', header: 'Tasks and Rota', subHeader:'Add individual tasks or view rota'},
  'Packages': {component: (<EmojiTransportationIcon fontSize="small"/>), pageComponent: (<EmojiTransportationIcon fontSize="large"/>), link: '/packages', header: 'Packages, Activities and Agents', subHeader:'Create agents and products belonging to them. Combine them with your products to create itineraries'},
  'Hotel Management': {component: (<RecordVoiceOverTwoToneIcon fontSize="small"/>), pageComponent: (<RecordVoiceOverTwoToneIcon fontSize="large"/>), link: '/hotel_management', header: 'Hotel Management', subHeader:"Control your team's user access, as well as managing hotel information"},
  'Settings and Reports': {component: (<SettingsIcon fontSize="small"/>), pageComponent: (<SettingsIcon fontSize="large"/>), link: '/settings', header: 'Settings and Reports', subHeader:'Generate Reports, Subscribe to Daily Reports and edit Account Settings'},

}

export default items;
