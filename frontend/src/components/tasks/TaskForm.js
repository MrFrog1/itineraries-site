import React, { Component } from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
// import { BookingForm } from '../../actions/bookings';


// identical logic to here: https://www.youtube.com/watch?v=BmL8iaLMnQ0&t=1419s

// class TaskForm extends Component {
//     state = {
//         guest: '',
//         hotel: '',
//         check_in: '',
//         check_out: ''
//     };

//     static propTypes = {
//         BookingForm: PropTypes.func.isRequired
//     };

//     onChange = e => this.setState({[e.target.name]: e.target.value});
    

//     onSubmit = e => {
//         e.preventDefault();
//         console.log('Submitted')
//         const { guest, hotel, check_in, check_out } = this.state;
//         const booking = { guest, hotel, check_in, check_out }    // doing this is the same as declaring name:name, check_in: check_in etc - destructuring
//         this.props.BookingForm(booking);

//     };

//     render() {
//         return (
//             <div className="card card-body mt-4 mb-4">
//                 <h1> Add Booking </h1>
//                 <form onSubmit={this.onSubmit}>
//                     <div className="form-group">
//                         <label>Guest:</label>  
//                         <br />
//                         <input className="form-control" type = "text" name="guest" onChange={this.onChange} value = {this.state.guest}/>
//                     </div>
//                     <div className="form-group">
//                         <label>Hotel: </label>
//                         <br />
//                         <input className="form-control" type = "text" name="hotel" onChange={this.onChange} value = {this.state.hotel}/>
//                     </div>
//                     <div>
//                         <label>Check In: </label>
//                         <br />
//                         <input className="form-control" type = "text" name="check_in" onChange={this.onChange} value = {this.state.check_in}/>
//                     </div>
//                     <div className="form-group">
//                         <label>Check Out: </label>
//                         <br />
//                         <input className="form-control" type = "text" name="check_out" onChange={this.onChange} value = {this.state.check_out}/>
//                     </div>
//                     <br />
//                     <button type = "submit" className="btn btn-primary"> Submit </button>
//                 </form>
//             </div>
//         )
//     }
// }

// export default connect(null, { BookingForm})(Task);
// // in the Bookings component, we had to to MapStatetoProps as we were bringing in state. We were bringing in 
// // bookings. With this, we are just calling the action so we put null (for mapStatetoProps) but we still need to add lead)