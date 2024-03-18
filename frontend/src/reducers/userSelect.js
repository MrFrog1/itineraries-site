import { USER_SELECT, LOG_OUT, USER_LOGIN, AUTH_ERROR, USER_LOADING, CHANGE_HOTEL_VIEW } from '../actions/types.js'

const initialState = {
    token: localStorage.getItem('token'),
    loggedIn: false,
    user: {},
    isLoading:true,
}   
    
const userReducer = (state= initialState,action) => {
    switch(action.type){
        case USER_LOADING:
            return {
                ...state,
                isLoading:true
            }
        case USER_LOGIN: //User login is for when the person logins first. User select is an ongoing thing
            return {
                ...state,
                loggedIn:true,
                isLoading:false,
                user: {...action.payload},


            }
        case USER_SELECT:
            return {
                ...state,
                loggedIn:true,
                isLoading:false,
                user: {...action.payload},


            }
        case AUTH_ERROR:
            return {
                ...state,
                token: null,
                user: null,
                isLoading: false,
                loggedIn: false
            }
        
        case LOG_OUT:
            return {
                ...state,
                token: null,
                user: null,
                isLoading: false,
                loggedIn: false
            }
       case CHANGE_HOTEL_VIEW:
            return {
                ...state,
                user: {...action.payload},
            }            

        default:
            return state

    }
}


export default userReducer