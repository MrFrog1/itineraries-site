import './App.css';
import React, { useEffect } from 'react';
import ReactDOM from 'react-dom/client';
// import './index.css';
import { Provider } from "react-redux";
import store from "../store";
import Routes from "./Routes.js";
// import { autoLogin } from "../actions/userActions";
import { BrowserRouter as Router } from "react-router-dom";


export default function App() {
  // useEffect(() => {
  //   store.dispatch(autoLogin());
  // }, []);  NEED TO CREATE THE AUTOLOGIN

  return (

    
    <Provider store={store}>
        <Router>
          <Routes />
        </Router>
    </Provider>


  );
}

ReactDOM.render(<App />, document.getElementById("app"));


