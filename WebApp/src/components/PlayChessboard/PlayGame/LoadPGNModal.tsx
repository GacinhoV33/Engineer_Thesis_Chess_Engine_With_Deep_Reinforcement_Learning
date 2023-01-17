import { Chess } from 'chess.js'
import React, { useState } from 'react'
import { Button, Modal } from 'react-bootstrap'
import InputGroup from 'react-bootstrap/InputGroup';
import Form from 'react-bootstrap/Form';

export interface LoadPGNModalProps{
    setGame: React.Dispatch<React.SetStateAction<Chess>>,
    setShowLoadModal: React.Dispatch<React.SetStateAction<boolean>>
    showLoadModal: boolean, 
}

const LoadPGNModal: React.FC<LoadPGNModalProps> = ({setGame, setShowLoadModal, showLoadModal}) => {
    const [value, setValue] = useState<string>('')
    
    function handleLoading(){
        console.log(value)
        const newGame = new Chess();
        newGame.loadPgn(value)
        setGame(newGame)
        setShowLoadModal(false)
    }

    return (
    <Modal show={showLoadModal} centered onHide={() => setShowLoadModal(false)}>
        <Modal.Title style={{textAlign: 'center', fontWeight: '700', fontSize: '3.25vh', color: '#444', marginTop: '1vh'}}>
          Insert PGN
        </Modal.Title>
        <Modal.Body style={{display: 'flex', flexDirection: 'row', alignItems: 'center', justifyContent: 'space-evenly'}}>
        <InputGroup>
            <InputGroup.Text onClick={handleLoading} style={{cursor: 'pointer', height: '10vh', fontWeight: '500'}}> Load </InputGroup.Text>
                <Form.Control as="textarea" aria-label="With textarea" value={value} onChange={(e) => setValue(e.target.value)}/>
            </InputGroup>
        </Modal.Body>
    </Modal>
  )
}

export default LoadPGNModal