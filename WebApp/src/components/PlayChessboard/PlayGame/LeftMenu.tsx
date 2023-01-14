import React, { useEffect, useState, useRef } from 'react'
import './LeftMenu.scss'
import Table from 'react-bootstrap/Table';
import { Chess } from 'chess.js';
export interface LeftMenuProps{
  game: Chess,
}

const LeftMenu: React.FC<LeftMenuProps> = ({game}) => {
  const [moves, setMoves] = useState<string[]>(Array());
  const [white, setWhite] = useState<string[]>(Array());
  const [black, setBlack] = useState<string[]>(Array());

  useEffect(() => {
    parsePGNToTable();
  }, [game])

  const handleScroll = () => {
    var element = document.getElementById('history');
    //@ts-ignore
    element.scrollTop = element.scrollHeight;

  };

  function parsePGNToTable(){
    const currentPGN = game.pgn();
    const arr = currentPGN.split(' ');
    const newMoves = [];
    const newWhite = []
    const newBlack = []
    for(let i = 0; i < arr.length; i++){
        if(i % 3 === 0){
          newMoves.push(arr[i])
        }
        else if(i % 3 === 1){
          newWhite.push(arr[i])
        }
        else{
          newBlack.push(arr[i])
        }
    }
    setMoves(newMoves)
    setWhite(newWhite)
    setBlack(newBlack)
    handleScroll() 
    return 
  }

  return (
    <div className='menu-header' >
     <div style={{position: 'sticky', color: '#EEE', textAlign: 'center', top: '0px', fontWeight: '600', fontSize: '2vh', marginBottom: '2vh'}}> GAME HISTORY </div> 
     <div className='main-left-menu' id='history'>
    <Table className='table-history'>
      <tbody >
        {
          moves.map((move, index) => (
            <tr key={moves[index]}>
              <td style={{width: '3vw'}} > {moves[index]} </td>
              <td style={{width: '6vw'}}> {white[index]} </td>
              {/* <td style={{width: '2vw'}}> {black} </td> */}
              {index + 1 <= black.length ? <td style={{width: '6vw'}}>{black[index]}</td> : <td style={{width: '6vw'}}></td>}
            </tr>
          ))
        }
        
      </tbody>
    </Table>
    </div>
    </div>
  )
}

export default LeftMenu