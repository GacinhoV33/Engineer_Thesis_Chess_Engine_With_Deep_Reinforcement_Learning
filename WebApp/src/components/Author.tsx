import React, { useEffect, useState } from 'react';
import AnimatedLetters from './AnimatedLetters';
import './Author.scss';


export interface AuthorProps{

}

const Author: React.FC<AuthorProps> = ({

}) => {
const [letterClass, setLetterClass] = useState<string>('text-animate')

setTimeout(() => {
    setLetterClass('text-animate-hover')
  }, 5500);

const name = 'Filip Gacek';
const job = 'Software Engineer'
return (
    <div className='mainAuthor'>
        <div className='content'>
        <h1>
            <AnimatedLetters
              letterClass={letterClass}
              text={`Welcome, I'm Filip Gacek`}
              idx={1}
            />
            <br />
            <AnimatedLetters
              letterClass={letterClass}
              text={job}
              idx={30}
            />
          </h1>
        </div>
        <div className='rightBar'>

        </div>
    </div>
  )
}





export default Author