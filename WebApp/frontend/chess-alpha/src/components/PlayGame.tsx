import React from 'react';
import PlayModes from './PlayModes';

export interface PlayGameProps{

}
export type PlayMode = 'Player-Engine' | 'Player-Player' | 'Engine-Engine' | 'None'

const PlayGame: React.FC<PlayGameProps> = ({}) => {
    const currentMode: PlayMode = 'None';
    return (
    <div>
        <PlayModes currentMode={currentMode}/>

    </div>
  )
}

export default PlayGame;