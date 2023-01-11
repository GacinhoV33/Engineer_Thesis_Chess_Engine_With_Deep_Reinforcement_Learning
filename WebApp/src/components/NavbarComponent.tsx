import React from 'react';
import './NavbarComponent.scss';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav'
import { Container } from 'react-bootstrap';

export interface NavbarComponentProps{

}

const NavbarComponent: React.FC<NavbarComponentProps> = ({}) => {
  return (
    <div className='navbar-main'>
        <Navbar>
          <Container>
            <Nav className='navContent'>
              <Navbar.Brand href="home" className='brand'>
                Deep Chess
                <img src={require('./images/logo_grey.png')} alt='logo' style={{width: '3vw'}}/>
              </Navbar.Brand>
              <Nav.Link href='play' className='navitem'>
                Play
              </Nav.Link>
              <Nav.Link href='engine' className='navitem'>
                Engine
              </Nav.Link>
              <Nav.Link href='thesis' className='navitem'>
                Thesis
              </Nav.Link>
              <Nav.Link href='about' className='navitem'>
                About
              </Nav.Link>
            </Nav>
          </Container>
          
        </Navbar>
    </div>
  )
}

export default NavbarComponent