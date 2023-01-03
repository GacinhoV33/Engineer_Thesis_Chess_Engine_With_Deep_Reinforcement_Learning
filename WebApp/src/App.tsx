import './App.css';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import PlayGame from './components/PlayGame';
import NavbarComponent from './components/NavbarComponent';
import 'bootstrap/dist/css/bootstrap.min.css';

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
<<<<<<< HEAD:WebApp/src/App.tsx
          fsakfkas
=======
          fsakfkas TEST
>>>>>>> 4c9b19948964672e3de429807b7a98f0ff1de4c4:WebApp/frontend/chess-alpha/src/App.tsx
        </Routes>
      </header>
    </div>
  );
}

export default App;
