import React, { useEffect, useState } from 'react'
import './LeftMenu.scss'
import Table from 'react-bootstrap/Table';
import { Chess } from 'chess.js';
import { move } from 'chessground/draw';
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

  function parsePGNToTable(){
    const currentPGN = game.pgn();
    const arr = currentPGN.split(' ');
    
    for(let i = 0; i < arr.length; i++){
        if(i % 3 === 0){
          moves.push(arr[i])
        }
        else if(i % 3 === 1){
          white.push(arr[i])
        }
        else{
          black.push(arr[i])
        }
    }
    console.log(white)
    return 
  }

  return (
    <div className='menu-header'>
     <div style={{position: 'sticky', color: '#EEE', textAlign: 'center', top: '0px', fontWeight: '600', fontSize: '2vh', marginBottom: '2vh'}}> GAME HISTORY </div> 
     <div className='main-left-menu'>
    <Table className='table-history'>
      <tbody>
      {/* <tbody>
        {
          black.map((black, index) => (
            <tr key={moves[index]}>
              <td style={{width: '2vw'}} > {moves[index]} </td>
              <td style={{width: '2vw'}}> {white[index]} </td>
              <td style={{width: '2vw'}}> {black} </td>
            </tr>
          ))
        } */}
        <tr>
          <td style={{width: '2vw'}}>1. </td>
          <td style={{width: '2vw'}}> Nf3 </td>
          <td style={{width: '2vw'}}>d6</td>
        </tr>
        <tr>
          <td>2. </td>
          <td style={{width: '2vw'}}> e3  </td>
          <td style={{width: '2vw'}}>a5</td>
        </tr>
        <tr>
          <td>3. </td>
          <td style={{width: '2vw'}}>g4  </td>
          <td style={{width: '2vw'}}>Nc6</td>
        </tr>
        <tr>
          <td>4. </td>
          <td style={{width: '2vw'}}>Nh4  </td>
          <td style={{width: '2vw'}}>Na7</td>
        </tr>
        <tr>
          <td>5. </td>
          <td style={{width: '2vw'}}>Be2  </td>
          <td style={{width: '2vw'}}>Nh6</td>
        </tr>
        <tr>
          <td>6. </td>
          <td style={{width: '2vw'}}>Rb1  </td>
          <td style={{width: '2vw'}}>e5</td>
        </tr>
        <tr>
          <td>7. </td>
          <td style={{width: '2vw'}}>Nb5  </td>
          <td style={{width: '2vw'}}>Qb8</td>
        </tr>
        <tr>
          <td>8. </td>
          <td style={{width: '2vw'}}> Rg1  </td>
          <td style={{width: '2vw'}}> c6</td>
        </tr>
        <tr>
          <td>9. </td>
          <td style={{width: '2vw'}}> a3  </td>
          <td style={{width: '2vw'}}>Bxg4</td>
        </tr>
        <tr>
          <td>10. </td>
          <td style={{width: '2vw'}}>Bc4  </td>
          <td style={{width: '2vw'}}>Kd8</td>
        </tr>
        <tr>
          <td>11. </td>
          <td style={{width: '2vw'}}>Bf1  </td>
          <td style={{width: '2vw'}}>f5</td>
        </tr>
        <tr>
          <td>12. </td>
          <td style={{width: '2vw'}}>b4  </td>
          <td style={{width: '2vw'}}>a4</td>
        </tr>
        <tr>
          <td>13. </td>
          <td style={{width: '2vw'}}>Rh1  </td>
          <td style={{width: '2vw'}}>Nxb5</td>
        </tr>
        <tr>
          <td>14. </td>
          <td style={{width: '2vw'}}>d4 </td>
          <td style={{width: '2vw'}}>Bh3 </td>
        </tr>
        <tr>
          <td>15. </td>
          <td style={{width: '2vw'}}>c4  </td>
          <td style={{width: '2vw'}}>Kd7 </td>
        </tr>
        <tr>
          <td>16. </td>
        </tr>
        <tr>
          <td>11. </td>
        </tr>
        <tr>
          <td>11. </td>
        </tr>
        <tr>
          <td>11. </td>
        </tr>
        <tr>
          <td>11. </td>
        </tr>
        <tr>
          <td>11. </td>
        </tr>
        <tr>
          <td>11. </td>
        </tr>
        <tr>
          <td>11. </td>
        </tr>
        <tr>
          <td>11. </td>
        </tr>
        <tr>
          <td>11. </td>
        </tr>
        <tr>
          <td>11. </td>
        </tr>
        <tr>
          <td>11. </td>
        </tr>
        <tr>
          <td>11. </td>
        </tr>
      </tbody>
    </Table>
    </div>
    </div>
   

    // <div className='left-menu'>
    //     <div className='header'>
    //        Game History
    //     </div>
    //     <div className='game-content'>
    //     1. Nf3 d6 2. e3 a5 3. Nc3 Bh3 4. g4 Nc6 5. Nh4 Na7 6. Be2 Nh6 7. Rb1 e5 8. Nb5 Qb8 9. Rg1 c6 10.
    //     a3 Bxg4 11. Bc4 Kd8 12. Bf1 f5 13. b4 a4 14. Rh1 Nxb5 15. d4 Bh3 16. c4 Kd7 17. f3 exd4 18. Bxh3
    //     Nc3 19. Qe2 Kc8 20. Qd2 Rg8 21. Bf1 Kd8 22. Qd1 d5 23. Rg1 Ra6 24. Qc2 Bc5 25. f4 Kc8 26. Qd1
    //     Kc7 27. Rxg7+ Be7 28. Kd2 dxe3+ 29. Kc2 b6 30. Rg5 Rh8 31. Bg2 Bf6 32. Qh1 Bd8 33. b5 Rg8 34.
    //     Kb2 Re8 35. Rg4 Kb7 36. Qd1 Nxb5 37. h3 Qc7 38. Qg1 Nxa3 39. Nf3 fxg4 40. Qh1 Kc8 41. Bf1 Rg8
    //     42. Ka1 gxh3 43. Nd2 e2 44. Bxa3 Qa7 45. Rc1 Qg7+ 46. Ka2 Kc7 47. Nf3 h2 48. Bb4 Qe7 49. Ne5
    //     Rg5 50. Bc5 Qf8 51. Qxh2 exf1=B 52. Be3 Nf5 53. Bc5 bxc5 54. Kb1 Rg6 55. Qh1 Kb7 56. Qe4 Qd6
    //     57. Qe3 Rb6+ 58. Ka1 Qe6 59. Rd1 Kc8 60. Rxd5 Be2 61. Nd7 Rg2 62. Nf6 Rf2 63. Qd4 Bxc4 64. Qd3
    //     Ne7 65. Qc3 h5 66. Qd4 Qf5 67. Rxd8+ Kb7 68. Rf8 Ra2.
    //     </div>
    // </div>
  )
}

export default LeftMenu