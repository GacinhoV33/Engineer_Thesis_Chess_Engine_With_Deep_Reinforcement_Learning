import React, { useState } from 'react'
import './Chessboard.scss';
import { Square, Chess, Piece } from 'chess.js';
import { Chessboard} from 'react-chessboard';
import deepcopy from 'deepcopy';

export interface ChessboardComponentProps{

}

const ChessboardComponent: React.FC<ChessboardComponentProps> = ({ }) => {
    
    const [game, setGame] = useState<Chess>(new Chess());
    function makeMove(move: any){
        const gameCopy = new Chess();
        gameCopy.loadPgn(game.pgn());
        const result = gameCopy.move(move);
        setGame(gameCopy);
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
        return true;
    }


    return (
    <div className='chessboard-main-styles'>
        <Chessboard position={game.fen()} onPieceDrop={onPieceDrop}/>
    </div>
  )
}

export default ChessboardComponent