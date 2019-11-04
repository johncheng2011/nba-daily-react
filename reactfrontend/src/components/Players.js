import React, {Component} from 'react';
import Player from './Player';


class Players extends Component {
    state = {  }
    
    render() { 
        return this.props.players.map((player) =>(  
          <Player key={player.playerid} player ={player} add={this.props.add} />   

        ));
    }
}
 
export default Players;