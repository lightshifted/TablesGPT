import Home from './pages/Home';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import './App.css';


function App() {
  return (
    <Router>
      <Switch>
        <Route path="/" exact component={Home} />
      </Switch>
    </Router>
  );
}

export default App;
