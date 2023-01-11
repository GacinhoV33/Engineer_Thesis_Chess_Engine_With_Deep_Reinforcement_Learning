import React, { useState } from "react";
import ChessboardComponent, { ChessColor } from "./Chessboard";
import PlayModes from "./PlayModes";
import "./PlayGame.scss";
import GameEvaluation from "./GameEvaluation";
import RightMenu from "./RightMenu";
import LeftMenu from "./LeftMenu";
import IOSSwitch from "./SwitchCustomed";
import { Chess, Move } from "chess.js";
import NewGameModal from "./NewGameModal";
import LoadPGNModal from "./LoadPGNModal";
import ShowResult, { Result } from "./ShowResult";

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
  const [lastMoveStack, setLastMoveStack] = useState<Move[]>([])
  const [result, setResult] = useState<Result>('none')  

  // AlphaZero Engine stuff

  function handleNewGame(){
    setShowModal(true);
  }

  function handleLoadPGN(){
    setShowLoadModal(true)
  }

  function handleUndo(){
    const undoMove = game.undo();
    if(undoMove) setLastMoveStack(prev => [...prev, undoMove]);
    const gameCopy = new Chess();
    gameCopy.loadPgn(game.pgn());
    setGame(gameCopy);
  }

  function handleDraw(){
    setGame(new Chess())
  }

  function handleGiveUp(){
    setGame(new Chess())
  }

  function handleEngine(){
    setIsStockfish(prev => !prev)
    setIsAlpha(prev => !prev)
  }

  function handleRedo(){
    const newGame = new Chess()
    newGame.loadPgn(game.pgn())
    const redoMove = lastMoveStack.pop();
    if(redoMove) {
      newGame.move(redoMove)
      setGame(newGame);
    }
  }

  return (
    <div className="playgame-main">
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
          <ChessboardComponent game={game} setGame={setGame} boardOrientation={boardOrientation} setResult={setResult}/>
        </div>
        <div style={{display: 'flex', flexDirection: 'column', gap: '1vh'}}>
          {result !== 'none' ? <div style={{textAlign: 'center'}}><ShowResult result={result}/> </div> : <h1> Null </h1>}

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
          <div style={{width: '50%', padding: '5%',}}>
              <div style={{display: 'flex', gap: '5px', justifyContent: 'center', alignItems: 'center', marginTop: '1vh'}}>
                <div 
                  style={{height: '3vh',  background: '#EEE', width: '40%', cursor: 'pointer', display: 'flex', justifyContent: 'center', alignItems: 'center'}}
                  className={boardOrientation === 'white' ? 'border-orientation' : undefined}
                  onClick={() => setBoardOrientation('white')}
                >
                </div>
                <div 
                  style={{height: '3vh',  background: '#000', width: '40%', cursor: 'pointer', display: 'flex', justifyContent: 'center', alignItems: 'center'}} 
                  className={boardOrientation === 'black' ? 'border-orientation' : undefined}
                  onClick={() => setBoardOrientation('black')}
                >
                </div>
              </div>
          </div>
          </div>
          <RightMenu handleNewGame={handleNewGame} handleLoadPGN={handleLoadPGN} handleUndo={handleUndo} handleDraw={handleDraw} handleGiveUp={handleGiveUp} handleRedo={handleRedo}/>
          {showModal && <NewGameModal setNewGame={setGame} showModal={showModal} setShowModal={setShowModal}/>}
          {showLoadModal && <LoadPGNModal setGame={setGame} setShowLoadModal={setShowLoadModal} showLoadModal={showLoadModal}/>}
        </div>
      </div>
    </div>
  );
};

export default PlayGame;
