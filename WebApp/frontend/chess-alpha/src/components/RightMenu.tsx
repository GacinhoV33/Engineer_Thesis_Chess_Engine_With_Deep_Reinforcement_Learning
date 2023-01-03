import React from 'react';
import './RightMenu.scss';
import Button from 'react-bootstrap/Button';

export interface RightMenuProps{

}

const RightMenu: React.FC<RightMenuProps> = ({}) => {
  return (
    <div className='right-menu'>
        <div style={{gridColumnStart: '1', gridColumnEnd: '2', gridRowStart: '1', gridRowEnd: '2', border: '1px solid white'}}>
            1
            Undo move
        </div>
        <div style={{gridColumnStart: '1', gridColumnEnd: '2', gridRowStart: '2', gridRowEnd: '3', border: '1px solid white'}}>
           2
           New game
           {/* After clicking open modal with color of piece. */}
        </div>
        <div style={{gridColumnStart: '1', gridColumnEnd: '2', gridRowStart: '3', gridRowEnd: '4', border: '1px solid white'}}>
            3. Stockfish - My Engine 
        </div>
        <div style={{gridColumnStart: '2', gridColumnEnd: '3', gridRowStart: '1', gridRowEnd: '2', border: '1px solid white'}}>
            4. Previous
        </div>
        <div style={{gridColumnStart: '2', gridColumnEnd: '3', gridRowStart: '2', gridRowEnd: '3', border: '1px solid white'}}>
            5
        </div>
        <div style={{gridColumnStart: '2', gridColumnEnd: '3', gridRowStart: '3', gridRowEnd: '4', border: '1px solid white'}}>
            6
        </div>
        <div style={{gridColumnStart: '3', gridColumnEnd: '4', gridRowStart: '1', gridRowEnd: '2', border: '1px solid white'}}>
            7
        </div>
        <div style={{gridColumnStart: '3', gridColumnEnd: '4', gridRowStart: '2', gridRowEnd: '3', border: '1px solid white'}}>
            8
        </div>
        <div style={{gridColumnStart: '3', gridColumnEnd: '4', gridRowStart: '3', gridRowEnd: '4', border: '1px solid white'}}>
            9
        </div>
    </div>
  )
}

export default RightMenu