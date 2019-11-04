import React from 'react';
import axios from 'axios';
import {BrowserRouter as Router,Route} from 'react-router-dom';
import {Link} from 'react-router-dom';
// import './App.css';
import "tabler-react/dist/Tabler.css";
import Players from './components/Players';
import SiteWrapper from './components/Header';
import Home from './components/pages/Home';
import PlayersPerGame from './components/pages/PlayersPerGame';
import PlayersZScores from './components/pages/PlayersZScores';
import AllPerGame from './components/pages/AllPerGame';
import AllZscores from './components/pages/AllZscores';

import About from './components/pages/About';
class App extends React.Component{
  state = {
    players: []
  }
  
  // componentDidMount() {
  //   //axios.get('http://localhost:5000/_allPlayerPerGame')
  //   axios.get('/_allPlayerPerGame')
  //   .then(res => this.setState({players: res.data}))
  //   }
 
  
  add = (id) =>{
    this.setState({players: this.state.players.map(player => {
      if(player.playerid === id){
        player.ast += 1;
      }
      return player;
    })})
  }

  render(){
    return (
      <Router>
        <div className = "container">
          <Route exact path = "/" component={Home} />

          <Route path = '/about' render = {props=>(
            <React.Fragment>
              <About />

            </React.Fragment>

          )}/>
          <Route path = '/players/:date' component={PlayersPerGame}/>
          <Route path = '/zscores/:date' component={PlayersZScores}/>
          <Route path = '/all_players_pergame' component = {AllPerGame}/>
          <Route path = '/all_players_zscores' component = {AllZscores}/>
        </div>
      </Router>
    );
  }
  }
  export default App;
//original
// function App() {
//   state = {
//     players: []
//   }
//   return (
//     <div className="App">
//       <h1>hello this.state</h1>
//     </div>
//   );
// }
//import logo from './logo.svg';
/* <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header> */