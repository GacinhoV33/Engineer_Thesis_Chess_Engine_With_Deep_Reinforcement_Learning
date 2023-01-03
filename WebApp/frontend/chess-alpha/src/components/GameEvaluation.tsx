import React from 'react'
import ProgressBar from 'react-bootstrap/ProgressBar';

export type Engine = 'MyEngine' | 'Stockfish'

export interface GameEvaluationProps{
    value: number,
    engineType: Engine
}

function evalToProgress(value: number){
    return 50 - value * 50;
}

const GameEvaluation: React.FC<GameEvaluationProps> = ({value, engineType}) => {
  // TODO evaluation for stockfish and my engine
  return (
    <div style={{width: '75vh', margin: '0 1vh'}}>
        <ProgressBar now={evalToProgress(value)} label={value > 0 ? `+${value}` : `${value}`} variant='secondary'/>
    </div>
  )
}

export default GameEvaluation