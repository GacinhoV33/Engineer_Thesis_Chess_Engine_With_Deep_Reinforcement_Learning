import React from 'react';
import './NavbarComponent.scss';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav'
import { Container } from 'react-bootstrap';
// import logo_chess from './';

export interface NavbarComponentProps{

}

const NavbarComponent: React.FC<NavbarComponentProps> = ({}) => {
  return (
    <div className='navbar-main'>
        <Navbar fixed='top' >
          <Container>
            <Nav className='navContent'>
              <Navbar.Brand href="home" className='brand'>
                Deep Chess
                <img src={require('./logo_grey.png')} alt='logo' style={{width: '3vw'}}/>
              </Navbar.Brand>
              <Nav.Link href='play' className='navitem'>
                Play
              </Nav.Link>
              <Nav.Link href='engine' className='navitem'>
                Engine
              </Nav.Link>
              <Nav.Link href='about' className='navitem'>
                About Author
              </Nav.Link>
            </Nav>
          </Container>
          
        </Navbar>
    </div>
  )
}

export default NavbarComponent