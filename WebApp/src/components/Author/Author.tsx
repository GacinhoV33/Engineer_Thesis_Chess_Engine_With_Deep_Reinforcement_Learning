import React, { useState } from 'react';
import AnimatedLetters from '../AnimatedLetters';
import './Author.scss';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faGithub, faLinkedin, faGoogle, faReact, faHtml5, faSass, faPython, faDocker } from '@fortawesome/free-brands-svg-icons';
//@ts-ignore
import ReactRoundedImage from 'react-rounded-image';
import Alert from 'react-bootstrap/Alert';
import {AiOutlineCopy} from 'react-icons/ai';
import {SiTypescript} from 'react-icons/si';
import {SiMicrosoftazure} from 'react-icons/si';
import useAnalyticsEventTracker from '../../useAnalyticsEventTracker';

export interface AuthorProps{

}

const Author: React.FC<AuthorProps> = ({

}) => {
const [letterClass, setLetterClass] = useState<string>('text-animate')
const [showAlert, setShowAlert] = useState<boolean>(false)
const [opacityLevel, setOpacityLevel] = useState<number>(0)
setTimeout(() => {
    setLetterClass('text-animate-hover')
  }, 5500);

setTimeout(() => {
  if(opacityLevel < 1){
    setOpacityLevel(prev => prev + 0.01);
  };
}, 32)

function copyEmailToClipboard(){
  // Do stuff 
  navigator.clipboard.writeText('gacek.filip12@gmail.com');
  setShowAlert(true);
  setTimeout(() => {
    setShowAlert(false)
  }, 4000);
}
const gaEventTracker = useAnalyticsEventTracker('new_game');

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
          <span style={{opacity: opacityLevel}}>

          <p style={{marginBottom: '5vh'}}>
            I graduated Automatics Control and Robotics on AGH University of Science and Technology in 2023. Currently I am doing master's degree in Computer Science. 
            <br></br>I focus my career in fields of web development and artificial intelligence. In my free time I enjoy creating my own applications, discover beauty of AI and play chess. 
            <br></br>My hobbies motivated me to chose topic <i>Virtual Chess Engine using Reinforcement Learning</i>. 
            Present website contains results of my engineer's thesis. 
          </p>
          <h3 style={{marginBottom: '2vh'}}> Tech stack used in project: </h3>
          <div style={{display: 'flex', gap: '10vh'}}>
            <div style={{display: 'flex', flexDirection: 'column'}}>
              <div className='language'>
                  <FontAwesomeIcon 
                      icon={faReact} 
                      className='icon-stack'
                    />  
                    React
                </div>
                <div className='language'>
                  <SiTypescript className='icon-stack'/>
                    Typescript
                </div>
                <div className='language'>
                  <FontAwesomeIcon 
                      icon={faHtml5} 
                      className='icon-stack'
                    />  
                    HTML5
                </div>
                <div className='language'>
                  <FontAwesomeIcon 
                      icon={faSass} 
                      className='icon-stack'
                    />  
                    Sass
                </div>
            </div>
            <div style={{display: 'flex', flexDirection: 'column'}}>
            <div className='language'>
                <FontAwesomeIcon 
                    icon={faPython} 
                    className='icon-stack'
                  />  
                  Python
              </div>
              <div className='language'>
                <FontAwesomeIcon 
                      icon={faDocker} 
                      className='icon-stack'
                    />  
                  Docker
              </div>
              <div className='language'>
                  <SiMicrosoftazure className='icon-stack'/>
                  Azure
              </div>
          </div>
          </div>  
          </span>

        </div>
        <div style={{width: '0.1vw', borderLeft:  '1px solid #eee', height: '80%'}}></div>
        <div className='rightBar'>
        <h4 className='author-cite'> <q> The beauty of artificial intelligence should go in pair with great designs.</q> </h4>
          <div className='photo'>
            <ReactRoundedImage 
              image={require('../images/profile.png')}
              roundedColor="#EEE"
              imageWidth="275"
              imageHeight="275"
            />
          </div>
          <h3 style={{color: '#EEE'}}>Social media</h3>
          <div className='icons'>
          <a href='https://github.com/GacinhoV33/Filip_Gacek_Portfolio' target="_blank">
            <FontAwesomeIcon 
              icon={faGithub} 
              className='icon-social'
              />   
          </a>
          <a href='https://www.linkedin.com/in/filip-gacek-423799232/' target="_blank" 
            onClick={() => gaEventTracker('new_game')}
          >
            <FontAwesomeIcon 
              icon={faLinkedin} 
              className='icon-social'
            />     
          </a> 
           
          <FontAwesomeIcon 
            icon={faGoogle} 
            className='icon-social'
            onClick={copyEmailToClipboard}
          />    
          
          </div>
          {showAlert ? 
            <Alert variant='secondary'>
              <AiOutlineCopy size={24}/>
              gacek.filip12@gmail.com copied to the clipboard.
            </Alert> : <div style={{height: '8vh'}}> - </div>}
        </div>
    </div>
  )
}





export default Author