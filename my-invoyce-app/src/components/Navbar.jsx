import React from 'react'
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import { useAuth, logout } from '../auth'

const LoggedInLinks=()=>{
    return(
        <>
            <Nav.Link href="/">Home</Nav.Link>
            <Nav.Link href="/Create_Recipe">Create Recipe</Nav.Link>
            { <Nav.Link href="/" onClick={()=>{logout()}}>Log Out</Nav.Link> }
        </>
    )
}

const LoggedOutLinks=()=>{
    return(
        <>
            <Nav.Link href="/">Home</Nav.Link>
            <Nav.Link href="/signUp">Sign Up</Nav.Link>
            <Nav.Link href="/login">Login</Nav.Link>
        </>
    )
}

const NavBar =()=>{
    const[logged]=useAuth();
 
    return (
        <Navbar bg="dark" data-bs-theme="dark" fixed="top">
            <Container>
                <Navbar.Brand href="#home">Recipes</Navbar.Brand>
                <Nav className="me-auto">
                    {logged?<LoggedInLinks/>:<LoggedOutLinks/>}
                </Nav>
            </Container>
      </Navbar>
    );
}

export default NavBar
    