
// Needs to be changed to Hooks and would need a hotel ID first?

// import React, { Component } from 'react';
// import {Redirect, withRouter} from 'react-router-dom';
// import {connect} from 'react-redux';
// import {signUserUp} from '../../actions/userActions'

// class SignUp extends Component {
//     state = {
//         username: "",
//         password: "",
//         hotel_id: ""
//     }

//     handleOnChange = (e) => {
//         e.persist();
//         this.setState(() => ({
//             [e.target.name]: e.target.value 
//         }))
//     }

//     onSubmit = (e) => {
//         e.preventDefault()
//         this.props.signUserUp(this.state)
//     }

//     render(){
//         return(
//             <div>
//                 <h1>SignUp Form</h1>
//                 <Form onSubmit={this.onSubmit}>
//                     <input 
//                         type="text" 
//                         name="username" 
//                         placeholder="User Name" 
//                         value={this.state.username}
//                         onChange={this.handleOnChange}
//                     />
//                     <br/>
//                     <input
//                         type="password"
//                         name="password"
//                         placeholder="Password"
//                         value={this.state.password}
//                         onChange={this.handleOnChange}
//                     />
//                     <br/>
//                     <input
//                         type="text"
//                         name="hotel_id"
//                         placeholder="Hotel ID"
//                         value={this.state.hotel_id}
//                         onChange={this.handleOnChange}
//                     />

//                     <br/>
//                     <input
//                         type="submit"
//                         value="Login"
//                     />
//                 </Form>
//             </div>
//         )
//     }
// }

// const mapDispatchToProps = (dispatch) => {
//     return {
//         signUserUp: (userInfo) => dispatch(signUserUp(userInfo))
//     }
// }

// const ShowTheLocationWithRouter3 = withRouter(SignUp);

// export default connect(null, mapDispatchToProps)(ShowTheLocationWithRouter3)

