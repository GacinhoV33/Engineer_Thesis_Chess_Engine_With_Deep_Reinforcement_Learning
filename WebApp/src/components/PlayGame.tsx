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
import { ToggleButtonGroup } from "@mui/material";
import { ToggleButton } from "@mui/material";


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
  const [isStockfish, setIsStockfish] = useState<boolean>(false);
  const [boardOrientation, setBoardOrientation] = useState<ChessColor>('white')
  // const [isGameStarted, setGameIsStarted] = useState<boolean>(false); TODO?
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

  function handleEngine(){
    setIsStockfish(prev => !prev)
    setIsAlpha(prev => !prev)
  }

  function handleColor(requestedColor: ChessColor){
    if(requestedColor !== boardOrientation){
      if(boardOrientation === 'white'){
        setBoardOrientation('black')
      }
      else{
        setBoardOrientation('white')
      }
    }
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
                <img src={require('./images/chess2.png')} alt='lol' style={{width: '1vw'}}/>
              </div>
              <GameEvaluation value={isAlpha ? -0.2 : 0.2} engineType='MyEngine'/>
              <div style={{width: '1vw'}}>
                <img src={require('./images/chess1.png')} alt='lol' style={{width: '1vw'}}/>
              </div>
            </div>
          </div>
          <ChessboardComponent game={game} setGame={setGame} boardOrientation={boardOrientation}/>
        </div>
        <div style={{display: 'flex', flexDirection: 'column', gap: '1vh'}}>
          <div style={{display: 'flex'}}>
          <div style={{display: 'flex', flexDirection: 'column', gap: '1vh', color: '#EEE', fontSize: '1.25vw', width: '50%', fontWeight: '500', paddingLeft: '5px'}}>
              <div style={{display: 'flex', alignItems: 'center', gap: '1vw', justifyContent: 'space-between'}}>
                  Stockfish
                  <IOSSwitch onClick={handleEngine} checked={isStockfish}/>
              </div>
              <div style={{display: 'flex', alignItems: 'center', gap: '1vw', justifyContent: 'space-between'}}>
                  AlphaZero
                  <IOSSwitch  defaultChecked  onClick={handleEngine} checked={isAlpha}/>
              </div>
          </div>
          <div style={{width: '50%', padding: '5%'}}>
            <ToggleButtonGroup color='standard' value={1} exclusive aria-label="Platform">
              <ToggleButton value={0} style={{border: '1px solid #EEE'}} onClick={() => handleColor('white')}> White </ToggleButton>
              <ToggleButton value={1} style={{background: '#EEE'}} onClick={() => handleColor('black')}>Black</ToggleButton>
            </ToggleButtonGroup>
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
