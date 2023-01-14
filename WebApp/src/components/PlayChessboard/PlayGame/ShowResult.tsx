import React from 'react'
import AnimatedLetters from '../../AnimatedLetters'
import '../../AnimatedLetters.scss';
export type Result = 'White' | 'Black' | 'Draw' | 'none'

export interface ShowResultProps{
    result: Result
}

const ShowResult: React.FC<ShowResultProps> = ({result}) => {
const text = result + ' Won';
return (
    <h1>
    <AnimatedLetters text={text} idx={1} letterClass='text-animate'/>
    </h1>
  )
}

export default ShowResult