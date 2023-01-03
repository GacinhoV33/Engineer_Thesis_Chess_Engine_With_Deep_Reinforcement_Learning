import './App.css';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import PlayGame from './components/PlayGame';
import NavbarComponent from './components/NavbarComponent';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <NavbarComponent/>
        <Routes>
          <Route
            path='/play'
            element={<PlayGame/>}
          />
        </Routes>
      </header>
    </div>
  );
}

export default App;
