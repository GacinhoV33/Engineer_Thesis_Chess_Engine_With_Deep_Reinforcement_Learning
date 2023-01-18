import React, { useEffect, useState } from "react";
import ChessboardComponent, { ChessColor } from "../Chessboard/Chessboard";
import "./PlayGame.scss";
import GameEvaluation from "./GameEvaluation";
import RightMenu from "./RightMenu";
import LeftMenu from "./LeftMenu";
import IOSSwitch from "./SwitchCustomed";
import { Chess, Move } from "chess.js";
import NewGameModal from "./NewGameModal";
import LoadPGNModal from "./LoadPGNModal";
import ShowResult, { Result } from "./ShowResult";
import Spinner  from "react-bootstrap/Spinner";
import { SiGodotengine } from 'react-icons/si';

export type EngineType = 'AlphaZero' | 'Stockfish'
export interface PlayGameProps {

}
export type PlayMode =
  | "Player-Engine"
  | "Player-Player"
  | "Engine-Engine"
  | "None";

export type GameStatus = 'not-started' | 'ongoing' | 'ended'


const API_URL = 'http://127.0.0.1:5000/'

const PlayGame: React.FC<PlayGameProps> = ({}) => {
  const [game, setGame] = useState<Chess>(new Chess());
  const [showModal, setShowModal] = useState<boolean>(false);
  const [showLoadModal, setShowLoadModal] = useState<boolean>(false);
  const [isAlpha, setIsAlpha] = useState<boolean>(true);
  const [isStockfish, setIsStockfish] = useState<boolean>(false);
  const [boardOrientation, setBoardOrientation] = useState<ChessColor>('white')
  const [lastMoveStack, setLastMoveStack] = useState<Move[]>([]);
  const [result, setResult] = useState<Result>('none');
  const [gameStatus, setGameStatus] = useState<GameStatus>('not-started');
  const [userPieceColor, setUserPieceColor] = useState<ChessColor>('white');
  const [boardTurn, setBoardTurn] = useState<ChessColor>('white');
  


  // AlphaZero Engine stuff
  const startingFen: string = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1';
  const [lastFiveFen, setLastFiveFen] = useState<string[]>(['rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1']);
  const [engine, setEngine] = useState<EngineType>('AlphaZero');
  const [evaluation, setEvaluation] = useState<number>(0);
  const [depth, setDepth] = useState<number>(1);
  const [engineStatus, setEngineStatus] = useState<boolean>(false);
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
    setEngineStatus(false);
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
      setEngineStatus(false);
    }
  }

  function handleNewGameModal(color: ChessColor) {
    setGame(new Chess());
    setUserPieceColor(color);
    setBoardOrientation(color);
    setGameStatus('not-started');
    setShowModal(false);
    setBoardTurn('white');
    setEvaluation(0);
    setEngineStatus(false);
  }

  useEffect(() => {
    if(game.fen() === startingFen){
      setGameStatus('not-started');
    }
    else if(game.isCheckmate() || game.isDraw() || game.isStalemate()){
      setGameStatus('ended');
    }
    else{
      setGameStatus('ongoing');
    }
  }, [game])

  const requestBestMoveOptions = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    }, 
    body: JSON.stringify({
      positions: lastFiveFen.join(';'),
      engine: engine,
      depth: depth
    })
  }

  const requestEvalOptions = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    }, 
    body: JSON.stringify({
      positions: lastFiveFen.join(';'),
      engine: engine,
      depth: depth
    })
  }

  useEffect( () => {
    const makeEngineMove = async () => {
      const data = await ( await fetch(API_URL + `best_move`, requestBestMoveOptions)).json();
      const gameCopy = new Chess();
      gameCopy.loadPgn(game.pgn());
      const move = {
          from: data.bestMove.slice(0, 2),
          to: data.bestMove.slice(2, 4),
        }
      const result = gameCopy.move(move);
      if(result){
        setGame(gameCopy);
        boardTurn === 'white' ? setBoardTurn('black') : setBoardTurn('white');
        setEngineStatus(false)
      }
    }

    const getEvaluation = async () => {
      const data = await ( await fetch(API_URL + `pos_eval`, requestEvalOptions)).json();
      const evaluation_data = Number(data.evaluation);
      setEvaluation(evaluation_data);
    }
    if(boardTurn !== userPieceColor) {
      makeEngineMove()
    }
    getEvaluation();

  }, [boardTurn]);
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
                <img src={require('../../images/chess2.png')} alt='lol1' style={{width: '1vw'}}/>
                
              </div>
              <GameEvaluation value={evaluation} engineType='MyEngine'/>
              <div style={{width: '1vw'}}>
                <img src={require('../../images/chess1.png')} alt='lol2' style={{width: '1vw'}}/>
              </div>
            </div>
          </div>
          <ChessboardComponent 
          game={game} 
          setGame={setGame} 
          boardOrientation={boardOrientation} 
          setResult={setResult} 
          boardTurn={boardTurn} 
          setBoardTurn={setBoardTurn} 
          lastFiveFen={lastFiveFen} 
          setLastFiveFen={setLastFiveFen}
          userPieceColor={userPieceColor}
          setEngineStatus={setEngineStatus}
          />
        </div>
        <div style={{display: 'flex', flexDirection: 'column', gap: '1vh'}}>
          {result !== 'none' ? <div style={{textAlign: 'center'}}><ShowResult result={result}/> </div> : <div style={{height: '5vh'}}></div>}

          <div style={{display: 'flex'}}>
          <div style={{display: 'flex', flexDirection: 'column', gap: '1vh', color: '#EEE', fontSize: '1.25vw', width: '50%', fontWeight: '500', paddingLeft: '5px'}}>
              <div style={{display: 'flex', alignItems: 'center', gap: '1vw', justifyContent: 'space-between'}}>
                  Stockfish
                  <IOSSwitch onClick={handleEngine} checked={isStockfish}/>
              </div>
              <div style={{display: 'flex', alignItems: 'center', gap: '1vw', justifyContent: 'space-between'}}>
                  AlphaZero
                  <IOSSwitch onClick={handleEngine} checked={isAlpha}/>
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
          {engineStatus ? <div className="engineSpinner">
            <SiGodotengine className="engineIcon"/>
            <span className="engineText">Engine is thinking </span> 
            <Spinner/>
          </div> : <div style={{height: '10vh'}}> </div>}
          {showModal && <NewGameModal setNewGame={setGame} showModal={showModal} setShowModal={setShowModal} setEngine={setEngine} engine={engine} handleNewGame={handleNewGameModal} setDepth={setDepth} depth={depth}/>}
          {showLoadModal && <LoadPGNModal setGame={setGame} setShowLoadModal={setShowLoadModal} showLoadModal={showLoadModal}/>}

        </div>
      </div>
    </div>
  );
};

export default PlayGame;
