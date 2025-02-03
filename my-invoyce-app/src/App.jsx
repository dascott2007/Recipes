import 'bootstrap/dist/css/bootstrap.min.css';
// import { useState, useEffect  } from 'react'
import './App.css'
import './styles/main.css'
import NavBar from './components/Navbar';
import {
  BrowserRouter as Router,
  Routes, //instead of switch
  Route
} from 'react-router-dom'
import SignUpPage from './components/SignUp';
import LoginPage from './components/Login';
import CreateRecipePage from './components/CreateRecipe';
import HomePage from './components/home';
//import HomePage from './components/Home';


const App=()=>{
  return(
    <Router>
      <div className="container">
        <NavBar/>
        <Routes>
          <Route path='/create_recipe' element={<CreateRecipePage />} />
          <Route path='/login' element={<LoginPage />} />
          <Route path='/signUp' element={<SignUpPage />} />
          <Route path='/' element={<HomePage />} />
        </Routes>
      </div>
    </Router>
    
  )
}


export default App
