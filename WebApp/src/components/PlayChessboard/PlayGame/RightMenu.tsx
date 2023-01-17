import React, { useState } from 'react';
import './RightMenu.scss';
import {GrUndo, GrRedo} from 'react-icons/gr';
import 'bootstrap/dist/css/bootstrap.min.css';
import {BsCheckLg, BsX} from 'react-icons/bs';

export interface RightMenuProps{
    handleNewGame: () => void,
    handleLoadPGN: () => void,
    handleUndo: () => void,
    handleDraw: () => void,
    handleGiveUp: () => void,
    handleRedo: () => void,
}

const RightMenu: React.FC<RightMenuProps> = ({handleNewGame, handleLoadPGN, handleUndo, handleDraw, handleGiveUp, handleRedo}) => {

const [showDraw, setShowDraw] = useState<boolean>(true);
const [showGiveUp, setShowGiveUp] = useState<boolean>(true);
    function handleDrawAutomat(isFirstClick: boolean = true, acceptDraw: boolean = false){
        if(!isFirstClick){
            if(acceptDraw){
                handleDraw();
            }
        } 
        else  setShowDraw(prev => !prev);
           
    }
    function handleGiveUpAutomat(isFirstClick: boolean = true, acceptGiveUp: boolean = false){
        if(!isFirstClick){
            if(acceptGiveUp){
                handleGiveUp();
            }
        } 
        else  setShowGiveUp(prev => !prev);
           
    }

  return (
    <div className='right-menu'>
        <div style={{gridColumnStart: '1', gridColumnEnd: '2', gridRowStart: '1', gridRowEnd: '2'}} onClick={handleNewGame}>
            <div className='menu-tile' >
                New Game
            </div>
        </div>
        <div style={{gridColumnStart: '1', gridColumnEnd: '2', gridRowStart: '2', gridRowEnd: '3'}} onClick={handleUndo}>
            <div className='menu-tile'>
                Undo
                <GrUndo/>
            </div>
        </div>
        <div style={{gridColumnStart: '2', gridColumnEnd: '3', gridRowStart: '1', gridRowEnd: '2'}} onClick={handleLoadPGN}>
            <div className='menu-tile'>
                Load PGN
            </div>
        </div>
        <div style={{gridColumnStart: '2', gridColumnEnd: '3', gridRowStart: '2', gridRowEnd: '3'}} onClick={handleRedo}>  
            <div className='menu-tile'>
                Redo
                <GrRedo/>
            </div>
        </div>
        <div style={{gridColumnStart: '1', gridColumnEnd: '2', gridRowStart: '3', gridRowEnd: '4'}} onClick={() => handleDrawAutomat()}>  
           <div className='menu-tile'>
            {
                showDraw ? 'Draw' : 
                <div style={{display: 'flex', flexDirection: 'row', gap: '20%', alignItems: 'center', justifyContent: 'center', height: '100%'}}>
                <div style={{ border: '1px solid #EEE', borderRadius: '15px', background: '#65C466', display: 'flex', justifyContent: 'center', alignItems: 'center', width: '3.5vw', height: '2vw'}}>
                    <BsCheckLg onClick={() => handleDrawAutomat(false, true)}/>
                </div>
                <div style={{border: '1px solid #EEE', borderRadius: '15px', background: 'red', display: 'flex', justifyContent: 'center', alignItems: 'center', width: '3.5vw', height: '2vw'}}>
                    <BsX size={40} onClick={() => handleDrawAutomat(false, false)}/>
                </div>
            </div>
            }
            </div> 
        </div>
        <div style={{gridColumnStart: '2', gridColumnEnd: '3', gridRowStart: '3', gridRowEnd: '4'}} onClick={() => handleGiveUpAutomat()}>  
            <div className='menu-tile'>
            {
                showGiveUp ? 'Give up' : 
                <div style={{display: 'flex', flexDirection: 'row', gap: '20%', alignItems: 'center', justifyContent: 'center', height: '100%'}}>
                <div style={{ border: '1px solid #EEE', borderRadius: '15px', background: '#65C466', display: 'flex', justifyContent: 'center', alignItems: 'center', width: '3.5vw', height: '2vw'}}>
                    <BsCheckLg onClick={() => handleGiveUpAutomat(false, true)}/>
                </div>
                <div style={{border: '1px solid #EEE', borderRadius: '15px', background: 'red', display: 'flex', justifyContent: 'center', alignItems: 'center', width: '3.5vw', height: '2vw'}}>
                    <BsX size={40} onClick={() => handleGiveUpAutomat(false, false)}/>
                </div>
            </div>
            }
            </div>
        </div>
    </div>
  )
}

export default RightMenu