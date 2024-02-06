import React, { Component, useEffect } from 'react';
import ReactDOM from 'react-dom';
// import store from "../store";
// import Routes from "./Routes.js";
// import { autoLogin } from "../actions/userActions";
import { BrowserRouter as Router } from "react-router-dom";
import { Provider } from "react-redux";




export default function App() {
//   useEffect(() => {
//     store.dispatch(autoLogin());
//   }, []);

  return (
    
    <div>
        <h1> React App</h1>

    </div>    

    // {/* <Provider store={store}>
    //   {/* <AlertProvider template={AlertTemplate} {...alertOptions}> */}
    //     <Router>
    //       <Routes />
    //     </Router>
    //   {/* </AlertProvider> */}
    // </Provider> */}

  );
}


ReactDOM.render(<App/>, document.getElementById('app'));