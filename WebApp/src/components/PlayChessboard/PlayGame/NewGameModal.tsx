import { Chess } from "chess.js";
import React, { useState } from "react";
import Pagination from "react-bootstrap/Pagination";
import Modal from "react-bootstrap/Modal";
import { EngineType } from "./PlayGame";
import "./NewGameModal.scss";
import { ChessColor } from "../Chessboard/Chessboard";
export interface NewGameModalProps {
  setNewGame: React.Dispatch<React.SetStateAction<Chess>>;
  showModal: boolean;
  setShowModal: React.Dispatch<React.SetStateAction<boolean>>;
  engine: EngineType;
  setEngine: React.Dispatch<React.SetStateAction<EngineType>>;
  handleNewGame: (color: ChessColor) => void,
  depth: number,
  setDepth: React.Dispatch<React.SetStateAction<number>>,
}

const NewGameModal: React.FC<NewGameModalProps> = ({
  showModal,
  setNewGame,
  setShowModal,
  engine,
  setEngine,
  handleNewGame,
  setDepth,
  depth,

}) => {


  return (
    <Modal show={showModal} centered onHide={() => setShowModal(false)}>
      <Modal.Title
        style={{
          textAlign: "center",
          background: "#262421",
          color: "#AAA",
          height: "10vh",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        Play with Engine
      </Modal.Title>
      <Modal.Body
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "space-evenly",
          height: "35vh",
          background: "#302E2C",
        }}
      >
        <div
          style={{
            width: "18vw",
            display: "flex",
            color: "#AAA",
            justifyContent: "center",
            fontSize: "2.1vh",
          }}
        >
          <div
            style={{
              border: "1px solid #AAA",
              width: "8vw",
              height: "5vh",
              textAlign: "center",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              cursor: "pointer",
            }}
            onClick={() => setEngine("Stockfish")}
            className={engine === "Stockfish" ? "engineOn" : "engineOff"}
          >
            MinMax
          </div>
          <div
            style={{
              border: "1px solid #AAA",
              width: "8vw",
              height: "5vh",
              textAlign: "center",
              alignItems: "center",
              display: "flex",
              justifyContent: "center",
              cursor: "pointer",
            }}
            onClick={() => setEngine("AlphaZero")}
            className={engine === "AlphaZero" ? "engineOn" : "engineOff"}
          >
            AlphaZero
          </div>
        </div>

        {engine === "Stockfish" ? (
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <div
              style={{
                color: "#BABABA",
                fontSize: "2.5vh",
                textAlign: "center",
                marginTop: "5px",
              }}
            >
              {" "}
              Level{" "}
            </div>
            <div
              style={{
                display: "flex",
                flexDirection: "row",
                marginTop: "0",
                height: "10vh",
                width: "100%",
                alignItems: "flex-start",
                justifyContent: "center",
                paddingTop: "5px",
              }}
            >
              <Pagination>
                {[1, 2, 3, 4, 5].map((level) => (
                  <Pagination.Item
                    key={level}
                    active={depth === level}
                    onClick={() => setDepth(level)}
                  >
                    {level}
                  </Pagination.Item>
                ))}
              </Pagination>
            </div>
          </div>
        ) : (
          <div style={{ height: "14vh" }}></div>
        )}
        <div
          style={{
            display: "flex",
            flexDirection: "row",
            width: "15vw",
            justifyContent: "space-evenly",
            marginBottom: '20px'
          }}
        >
          <div>
            <img
              src={require("../../images/chess2.png")}
              alt="lol1"
              style={{ width: "2.5vw", cursor: "pointer" }}
              onClick={() => handleNewGame('black')}
            />
          </div>
          <div>
            <img
              src={require("../../images/chess1.png")}
              alt="lol2"
              style={{ width: "2.5vw", cursor: "pointer" }}
              onClick={() => handleNewGame('white')}
            />
          </div>
        </div>
      </Modal.Body>
    </Modal>
  );
};

export default NewGameModal;
