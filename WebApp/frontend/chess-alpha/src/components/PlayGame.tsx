import React from "react";
import ChessboardComponent from "./Chessboard";
import PlayModes from "./PlayModes";
import "./PlayGame.scss";
import GameEvaluation from "./GameEvaluation";
import RightMenu from "./RightMenu";
import LeftMenu from "./LeftMenu";
export interface PlayGameProps {}
export type PlayMode =
  | "Player-Engine"
  | "Player-Player"
  | "Engine-Engine"
  | "None";

const PlayGame: React.FC<PlayGameProps> = ({}) => {
  const currentMode: PlayMode = "None";
  return (
    <div className="playgame-main">
      <PlayModes currentMode={currentMode} />
      <div className="chessboard-menu-position">
        <LeftMenu />
        <div className="chessboard-and-eval">
          <div style={{color: 'white', display: "flex", justifyContent: 'center', alignItems: 'center'}}>
            <div style={{width: '1vh'}}>
              B
            </div>
            <GameEvaluation value={-0.2} engineType='MyEngine'/>
            <div style={{width: '1vh'}}>
              W
            </div>
          </div>
          <ChessboardComponent />
        </div>
        <RightMenu />

      </div>
    </div>
  );
};

export default PlayGame;
