import './App.css';
import { Route, Routes } from "react-router-dom";
import PlayGame from './components/PlayChessboard/PlayGame/PlayGame';
import NavbarComponent from './components/Navbar/NavbarComponent';
import 'bootstrap/dist/css/bootstrap.min.css';
import Thesis from './components/Thesis/Thesis';
import Author from './components/Author/Author';
import ReactGA from 'react-ga';

const TRACKING_ID = "G-34MLQ8JJQQ"; // OUR_TRACKING_ID
ReactGA.initialize(TRACKING_ID);

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <NavbarComponent/>
        <Routes>
          <Route
            path='/'
            element={<PlayGame/>}
          />
          <Route
            element={<Thesis/>}
            path='/thesis'
          />
          <Route
            element={<Author/>}
            path='/about'
          />
        </Routes>
      </header>
    </div>
  );
}

export default App;
