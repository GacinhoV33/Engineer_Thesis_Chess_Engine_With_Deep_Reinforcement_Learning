import React from 'react'
import { PlayMode } from './PlayChessboard/PlayGame/PlayGame'

export interface PlayModesProps{
    currentMode: PlayMode,
}

const PlayModes: React.FC<PlayModesProps> = ({currentMode}) => {
  return (
    <div>PlayModes</div>
  )
}

export default PlayModes