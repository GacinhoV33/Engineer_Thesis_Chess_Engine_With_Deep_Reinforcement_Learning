import './App.css';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import PlayGame from './components/PlayGame';
import NavbarComponent from './components/NavbarComponent';
import 'bootstrap/dist/css/bootstrap.min.css';
import Thesis from './components/Thesis';
import Author from './components/Author';

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
