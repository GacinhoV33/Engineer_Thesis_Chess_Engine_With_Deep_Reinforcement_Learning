import React, { useState } from 'react';
import './Chessboard.scss';
import { Square, Chess, Piece, Move, Color } from 'chess.js';
import { Chessboard} from 'react-chessboard';
import deepcopy from 'deepcopy';
import {Howl, Howler} from "howler";
import ShowResult, { Result } from './ShowResult';

export type ChessColor = 'white' | 'black'

export interface ChessboardComponentProps{
    game: Chess,
    setGame: React.Dispatch<React.SetStateAction<Chess>>,
    boardOrientation: ChessColor,
    setResult: React.Dispatch<React.SetStateAction<Result>>,
    boardTurn: ChessColor,
    setBoardTurn:  React.Dispatch<React.SetStateAction<ChessColor>>,
    lastFiveFen: string[],
    setLastFiveFen: React.Dispatch<React.SetStateAction<string[]>>
}

const ChessboardComponent: React.FC<ChessboardComponentProps> = ({ game, setGame, boardOrientation, setResult, boardTurn, setBoardTurn, lastFiveFen, setLastFiveFen}) => {
    const sound = new Howl({
        src: require('./sounds/move_sound.wav')
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
        }
        
        if(gameCopy.isCheckmate()){
            if(gameCopy.turn() === 'w'){
                setResult('Black')
            }
            else{
                setResult('White')
            }
        }
        else if(gameCopy.isDraw()){
            setResult('Draw')
        }
        else{
            setResult('none')
        }
        
        return result;
    }

    function onPieceDrop(sourceSquare: Square, targetSquare: Square, piece: Piece){
        let move;
        //@ts-ignore
        if((piece === 'bP' || piece === 'wP') && (targetSquare.split('')[1] === '1' || targetSquare.split('')[1] === '8') ){
            console.log('Prom')
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
        sound.play()
        boardTurn === 'white' ? setBoardTurn('black') : setBoardTurn('white');
        return true;
    }


    return (
    <div className='chessboard-main-styles'>
        <Chessboard position={game.fen()} 
        // @ts-ignore
        onPieceDrop={onPieceDrop} boardOrientation={boardOrientation}/>
        {/* {result !== 'none' ? <div style={{textAlign: 'center'}}><ShowResult result={result}/> </div> : null} */}
    </div>
  )
}

export default ChessboardComponent