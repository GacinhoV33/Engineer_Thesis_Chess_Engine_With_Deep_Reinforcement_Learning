import React, { useState } from 'react';
import './Chessboard.scss';
import { Square, Chess, Piece } from 'chess.js';
import { Chessboard} from 'react-chessboard';
import deepcopy from 'deepcopy';
import {Howl, Howler} from "howler";
// import moveSound from './move_sound.wav'
export interface ChessboardComponentProps{
    game: Chess,
    setGame: React.Dispatch<React.SetStateAction<Chess>>,
}

const ChessboardComponent: React.FC<ChessboardComponentProps> = ({ game, setGame }) => {
    const sound = new Howl({
        src: require('./move_sound.wav')
    })
    Howler.volume(0.7);
    function makeMove(move: any){
        const gameCopy = new Chess();
        gameCopy.loadPgn(game.pgn());
        const result = gameCopy.move(move);
        setGame(gameCopy);
        console.log(game.pgn())
        return result;
    }

    function onPieceDrop(sourceSquare: Square, targetSquare: Square){
        const move = makeMove({
            from: sourceSquare,
            to: targetSquare,
        });
        if (move === null){
            return false;
        }
        sound.play()
        return true;
    }


    return (
    <div className='chessboard-main-styles'>
        <Chessboard position={game.fen()} onPieceDrop={onPieceDrop}/>
    </div>
  )
}

export default ChessboardComponent