import { GET_BOOKINGS, DELETE_BOOKING, ADD_BOOKING, UPDATE_BOOKING} from '../actions/types.js'


const initialState = {
    bookings: [],
};
    
export default function(state = initialState, action) {
    switch(action.type) {  //switch here looks at the action that has come in, sees its type and then creates actions dependent on which case it is. 
        case GET_BOOKINGS:
            return {
                ...state,  //this spread operator returns anything currently in the state
                bookings : action.payload
            };
        case DELETE_BOOKING:
            return {
                ...state,  //this spread operator returns anything in the state
                bookings : state.bookings.filter(booking => booking.id!== action.payload)
            };
        case ADD_BOOKING:
            return {
                bookings : [...state.bookings, action.payload] //this makes bookings any bookings that were already there, in addition to the payload, which is the booking we just added
            };
        case UPDATE_BOOKING:
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