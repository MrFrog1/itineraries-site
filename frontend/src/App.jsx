import './App.css'
import { store } from './app/store'
import './assets/fonts.css'
import { Provider } from 'react-redux'
import AppRoutes from "./components/routes/Routes.jsx";
import { BrowserRouter as Router } from "react-router-dom";

function App() {
  return (
    <Provider store={store}>
    <div className="App">
        <Router>
          <AppRoutes />
        </Router>
    </div>
    </Provider>

  )
}

export default App
