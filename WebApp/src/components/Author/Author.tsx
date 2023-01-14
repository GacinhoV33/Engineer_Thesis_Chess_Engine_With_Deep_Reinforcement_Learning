import React, { useEffect, useState } from 'react';
import AnimatedLetters from '../AnimatedLetters';
import './Author.scss';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faGithub, faLinkedin, faGoogle } from '@fortawesome/free-brands-svg-icons';


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
              text={`Welcome, I am Filip Gacek.`}
              idx={1}
            />
            {/* <AnimatedLetters
              letterClass={letterClass}
              text={job}
              idx={30}
            /> */}
          </h1>
          <p>
            I graduated Automatics Control and Robotics on AGH University of Science and Technology in 2023. <br></br>Currently I am doing master's degree in Computer Science.
            I focus my career in fields of web development and <br></br>artificial inteligence. In free time I enjoy creating my own applications. 
            <br></br>This website contains results of my engineer's thesis. I chose topic <i>Virtual Chess Engine using Reinforcement Learning</i> because of my passion to chess and willingness to 
            get familiar with Deep Reinforcement Learning methods and algorithms.
          </p>
          
        </div>
        <div className='rightBar'>
          <div className='photo'>

          </div>

          <h3 style={{color: '#EEE'}}>Social media</h3>
          <div className='icons'>
            
          <FontAwesomeIcon 
            icon={faGithub} 
            className='icon-social'
            />      
          <FontAwesomeIcon 
            icon={faLinkedin} 
            className='icon-social'
          />        
          <FontAwesomeIcon 
            icon={faGoogle} 
            className='icon-social'
            />    
          </div>
        </div>
    </div>
  )
}





export default Author