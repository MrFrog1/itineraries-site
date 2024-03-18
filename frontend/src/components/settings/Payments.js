import React, {Fragment} from 'react'
import { connect } from 'react-redux';

// Daily Info, Mini Calendar, Mini Tasks


export default function Dashboard() {
    return (
        <div>
            <h1> Welcome to the Dashboard </h1>

            {/* <h1>` Welcome to the Dashboard ${hotel}`</h1> */}
        </div>
    )
}

// const mapStateToProps = state => ({
//   authToken: state.currentUser && state.currentUser.authToken,
//   hotel: state.hotel_name
// });

// export connect(mapStateToProps)(ItemList);