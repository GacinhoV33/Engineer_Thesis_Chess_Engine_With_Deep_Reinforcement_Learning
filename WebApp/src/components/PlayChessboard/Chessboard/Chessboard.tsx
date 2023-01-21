import React, { useState } from 'react';
import './Chessboard.scss';
import { Square, Chess, Piece, Move, Color } from 'chess.js';
import { Chessboard} from 'react-chessboard';
import {Howl, Howler} from "howler";
import  { Result } from '../PlayGame/ShowResult';

export type ChessColor = 'white' | 'black'

export interface ChessboardComponentProps{
    game: Chess,
    setGame: React.Dispatch<React.SetStateAction<Chess>>,
    boardOrientation: ChessColor,
    setResult: React.Dispatch<React.SetStateAction<Result>>,
    boardTurn: ChessColor | 'none',
    setBoardTurn:  React.Dispatch<React.SetStateAction<ChessColor | 'none'>>,
    lastFiveFen: string[],
    setLastFiveFen: React.Dispatch<React.SetStateAction<string[]>>,
    userPieceColor: ChessColor,
    setEngineStatus: React.Dispatch<React.SetStateAction<boolean>>,
}

const ChessboardComponent: React.FC<ChessboardComponentProps> = ({ game, setGame, boardOrientation, setResult, boardTurn, setBoardTurn, lastFiveFen, setLastFiveFen, userPieceColor, setEngineStatus}) => {
    const sound = new Howl({
        src: require('../../sounds/move_sound.wav')
    })
    Howler.volume(0.7);
    function makeMove(move: Move){

        const gameCopy = new Chess();
        gameCopy.loadPgn(game.pgn());
        const result = gameCopy.move(move);
        setGame(gameCopy);
    
        if(result){
            lastFiveFen.splice(0, 1);
            setLastFiveFen(prev => [...prev, gameCopy.fen()])
            if(userPieceColor === boardTurn && !game.isGameOver()){
                setEngineStatus(true)
            }  
        }
        
        if(gameCopy.isCheckmate()){
            if(gameCopy.turn() === 'w'){
                setResult('Black');
                setEngineStatus(false);
                // setGameStatus('non-started')
            }
            else{
                setResult('White')
                setEngineStatus(false);
            }
        }
        else if(gameCopy.isDraw()){
            setResult('Draw');
            setEngineStatus(false);
        }
        else{
            setResult('none')
        }
        
        return result;
    }

    function onPieceDrop(sourceSquare: Square, targetSquare: Square, piece: Piece){
        let move;
        if(userPieceColor !== boardTurn) {return false}
        //@ts-ignore
        if((piece === 'bP' || piece === 'wP') && (targetSquare.split('')[1] === '1' || targetSquare.split('')[1] === '8') ){
            move = makeMove({
                from: sourceSquare,
                to: targetSquare,
                promotion: 'q' 
            } as Move);
        }
        else{
            move = makeMove({
                from: sourceSquare,
                to: targetSquare,
            } as Move);
        }
        if (move === null){
            return false;
        }
        boardTurn === 'white' ? setBoardTurn('black') : setBoardTurn('white');
        sound.play()
        return true;
    }


    return (
    <div className='chessboard-main-styles'>
        <Chessboard position={game.fen()} 
        // @ts-ignore
        onPieceDrop={onPieceDrop} boardOrientation={boardOrientation}/>
    </div>
  )
}

export default ChessboardComponent