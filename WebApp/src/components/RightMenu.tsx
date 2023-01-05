import React from 'react';
import './RightMenu.scss';
import Button from 'react-bootstrap/Button';
import {GrUndo, GrRedo} from 'react-icons/gr';
import IOSSwitch from './SwitchCustomed';
import 'bootstrap/dist/css/bootstrap.min.css';

export interface RightMenuProps{
    handleNewGame: () => void,
    handleLoadPGN: () => void,
    handleUndo: () => void,
}

const RightMenu: React.FC<RightMenuProps> = ({handleNewGame, handleLoadPGN, handleUndo}) => {
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
           {/* After clicking open modal with color of piece. */}
        </div>
        <div style={{gridColumnStart: '2', gridColumnEnd: '3', gridRowStart: '1', gridRowEnd: '2'}} onClick={handleLoadPGN}>
            <div className='menu-tile'>
                Load PGN
            </div>
        </div>
        <div style={{gridColumnStart: '2', gridColumnEnd: '3', gridRowStart: '2', gridRowEnd: '3'}}>  
            <div className='menu-tile'>
                Redo
                <GrRedo/>
            </div>
        </div>
        <div style={{gridColumnStart: '1', gridColumnEnd: '2', gridRowStart: '3', gridRowEnd: '4'}}>  
            <div className='menu-tile'>
                Draw
            </div>
        </div>
        <div style={{gridColumnStart: '2', gridColumnEnd: '3', gridRowStart: '3', gridRowEnd: '4'}}>  
            <div className='menu-tile'>
                Give up
            </div>
        </div>
    </div>
  )
}

export default RightMenu