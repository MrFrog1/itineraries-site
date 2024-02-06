import React, { Component, useEffect, Fragment } from "react";
import { withAlert } from "react-alert";
import { connect } from "react-redux";
import propTypes from "prop-types";

// dont refactor to hooks for time being, as prevProps isnt there. 

export class Alerts extends Component {
  static propTypes = {
    error: propTypes.object.isRequired
  };
  componentDidUpdate(prevProps, props) {
    const {error,alert} = this.props
    if(error !== this.prevProps.error) {
      if(error.msg.name)
      alert.error(`${error.msg}`)
      
      // // TRAVERSY HAS DIFFERENT, MORE SPECIFIC CODE HERE:
      // if (error!== this.prevProps.error) {
      //   if(error.msg.name) alert.error(`Name: ${error.msg.name.join()}`)
      // };
      //   if(error.msg.email) alert.error(`Email: ${error.msg.email.join()}`)
      // };  
      //   if(error.msg.message) alert.error(`Message: ${error.msg.message.join()}`)
      };  

    } 

  
  render() {
    return (<Fragment/>)
  }
}

const mapStateToProps = (state) => ({
  error: state.errors
})

export default connect(mapStateToProps)(withAlert()(Alerts));

