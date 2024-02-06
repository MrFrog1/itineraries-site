import { createStore, applyMiddleware} from 'redux';
import {composeWithDevTools} from 'redux-devtools-extension';
import * as thunk from 'redux-thunk';
import rootReducer from './reducers'   //dont need to specify index.js - webpack automatically looks there for the function


const initialState = {};

const middleware = [thunk.default];

const store = createStore(
    rootReducer, 
    initialState,
    composeWithDevTools(applyMiddleware(...middleware))
    );

export default store
 