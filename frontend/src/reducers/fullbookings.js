import { GET_FULL_BOOKINGS} from '../actions/types.js'


const initialState = {
    groupbookings: [],
    bookings: []
};

export default function(state = initialState, action) {
    switch(action.type) {
        case GET_FULL_BOOKINGS:
            return {
                ...state,  //this spread operator returns anything in the state
                bookings : action.payload.bookings
            };
        case DELETE_GROUP_BOOKING:
            return {
                ...state,  //this spread operator returns anything in the state
                bookings : state.bookings.filter(booking => booking.id!== action.payload)
            };
        case ADD_GROUP_BOOKING:
            return {
                ...state,  //this spread operator returns anything in the state
                bookings : [...state.bookings,action.payload] //this makes bookings any bookings that were already there, in addition to the payload, which is the booking we just added
            };
        case UPDATE_GROUP_BOOKING:
            return {
                ...state,  //this spread operator returns anything in the state
                bookings : [...state.bookings,action.payload]
                // action.payload may be wrong. maybe needs an ID to be brought in  
            };
        default:
            return state;
    }
}



// The action here comes from an actions folder. When an action is dispatched, it then uses the reducer function and the old state 