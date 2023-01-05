import { Chess } from "chess.js";
import React from "react";
import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";

export interface NewGameModalProps {
  setNewGame: React.Dispatch<React.SetStateAction<Chess>>;
  showModal: boolean,
  setShowModal: React.Dispatch<React.SetStateAction<boolean>>
}

const NewGameModal: React.FC<NewGameModalProps> = ({showModal, setNewGame, setShowModal}) => {
  
  function handleYes(){
    setNewGame(new Chess())
    setShowModal(false)
  }

  function handleNo(){
    setShowModal(false)
  }

  return (
    <Modal show={showModal} centered onHide={() => setShowModal(false)}>
        <Modal.Title style={{textAlign: 'center'}}>
          Do you really want start new game?
        </Modal.Title>
        <Modal.Body style={{display: 'flex', flexDirection: 'row', alignItems: 'center', justifyContent: 'space-evenly'}}>
          <Button variant='secondary' style={{width: '8vw'}} onClick={handleYes}>
            Yes
          </Button>
          <Button variant='secondary' style={{width: '8vw'}} onClick={handleNo}>
            No
          </Button>
        </Modal.Body>
    </Modal>
  );
};

export default NewGameModal;
