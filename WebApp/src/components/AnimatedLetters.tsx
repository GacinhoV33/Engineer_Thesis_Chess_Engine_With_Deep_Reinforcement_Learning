import React from 'react';
import './AnimatedLetters.scss';

export interface AnimatedLettersProps{
    letterClass: string,
    text: string,
    idx: number,
}

const AnimatedLetters: React.FC<AnimatedLettersProps> = ({letterClass, text, idx}) => {
  const arr = text.split('');
  console.log(arr)
  return (
    <span>
      {arr.map((letter, i) => (
        <span key={letter + i} className={`${letterClass} _${i + idx}`}>
          {letter}
        </span>
      ))}
    </span>
  )
}

export default AnimatedLetters