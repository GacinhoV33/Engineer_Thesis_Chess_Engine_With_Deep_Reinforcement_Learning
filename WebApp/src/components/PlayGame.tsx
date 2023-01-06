import React, { useState } from "react";
import ChessboardComponent, { ChessColor } from "./Chessboard";
import PlayModes from "./PlayModes";
import "./PlayGame.scss";
import GameEvaluation from "./GameEvaluation";
import RightMenu from "./RightMenu";
import LeftMenu from "./LeftMenu";
import IOSSwitch from "./SwitchCustomed";
import { Chess } from "chess.js";
import NewGameModal from "./NewGameModal";
import LoadPGNModal from "./LoadPGNModal";
// import chesspawn2 from "../chesspawn2.png";

export interface PlayGameProps {}
export type PlayMode =
  | "Player-Engine"
  | "Player-Player"
  | "Engine-Engine"
  | "None";

const PlayGame: React.FC<PlayGameProps> = ({}) => {
  const currentMode: PlayMode = "None";
  const [game, setGame] = useState<Chess>(new Chess());
  const [showModal, setShowModal] = useState<boolean>(false);
  const [showLoadModal, setShowLoadModal] = useState<boolean>(false);
  const [isAlpha, setIsAlpha] = useState<boolean>(true);
  const [boardOrientation, setBoardOrientation] = useState<ChessColor>('white')

  function handleNewGame(){
    setShowModal(true);
  }

  function handleLoadPGN(){
    setShowLoadModal(true)
  }

  function handleUndo(){
    game.undo();
    const gameCopy = new Chess();
    gameCopy.loadPgn(game.pgn());
    setGame(gameCopy);
  }

  function handleDraw(){
    //TODO show rezult somewhere
    setGame(new Chess())
  }

  function handleGiveUp(){
    setGame(new Chess())
  }

  return (
    <div className="playgame-main">
      {/* <PlayModes currentMode={currentMode} /> */}
      <div className="chessboard-menu-position">
        <LeftMenu game={game} />
        <div className="chessboard-and-eval">
          <div style={{color: 'white', display: "flex", justifyContent: 'center', alignItems: 'center', flexDirection: 'column'}}>
              <div style={{fontWeight: '500'}}>
                {isAlpha ? 'AlphaZero Evaluation' : 'Stockfish Evaluation'}
              </div>
            <div style={{display: 'flex', flexDirection: 'row', alignItems: 'center'}}>
              <div style={{width: '1vw'}}>
                <img src={require('./chess2.png')} alt='lol' style={{width: '1vw'}}/>
              </div>
              <GameEvaluation value={-0.2} engineType='MyEngine'/>
              <div style={{width: '1vw'}}>
                <img src={require('./chess1.png')} alt='lol' style={{width: '1vw'}}/>
              </div>
            </div>
          </div>
          <ChessboardComponent game={game} setGame={setGame} boardOrientation={boardOrientation}/>
        </div>
        <div style={{display: 'flex', flexDirection: 'column', gap: '1vh'}}>
          <div style={{display: 'flex', flexDirection: 'column', gap: '1vh', color: '#EEE', fontSize: '1.25vw', width: '50%', fontWeight: '500', paddingLeft: '5px'}}>
              <div style={{display: 'flex', alignItems: 'center', gap: '1vw', justifyContent: 'space-between'}}>
                  Stockfish
                  <IOSSwitch />
              </div>
              <div style={{display: 'flex', alignItems: 'center', gap: '1vw', justifyContent: 'space-between'}}>
                  AlphaZero
                  <IOSSwitch  defaultChecked />
              </div>
          </div>
          <RightMenu handleNewGame={handleNewGame} handleLoadPGN={handleLoadPGN} handleUndo={handleUndo} handleDraw={handleDraw} handleGiveUp={handleGiveUp}/>
          {showModal && <NewGameModal setNewGame={setGame} showModal={showModal} setShowModal={setShowModal}/>}
          {showLoadModal && <LoadPGNModal setGame={setGame} setShowLoadModal={setShowLoadModal} showLoadModal={showLoadModal}/>}
        </div>
      </div>
    </div>
  );
};

export default PlayGame;
