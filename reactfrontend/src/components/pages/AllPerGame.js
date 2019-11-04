import React, { Component } from 'react';
import axios from 'axios';
import PerGameTable from '../PerGameTable';
import SiteWrapper from '../Header';
// import Table from 'tabler-react';


export class PlayersPerGame extends Component {
    
    state={
        players:[],
    }
    log = (attr)=>{
        this.setState({players: this.state.players.sort(function(a,b) {
            var x = a[attr];
            var y = b[attr];
            return ((x < y) ? 1 : ((x > y) ? -1 : 0));

        }) })
    }

      componentDidMount() {
        // var   url = 'http://localhost:5000/_players/' + this.props.match.params.date;
        // var url = 'http://localhost:5000/_allPerGame'
        var   url = '/_allPerGame'
        axios.get(url)
        // axios.get('/_allPlayerPerGame')
        .then(res => this.setState({players: res.data}))
        
        }

    

    render() {
        console.log(this.state.players)
        return (
            <SiteWrapper>
            <div className = "container">
                
                {/* <table>
                    <thead>
                      <th onClick = {this.log}>fdf</th>  
                      <th>sdd</th>
                      <th>count</th>
                    </thead>
                    <tbody>
                        {this.state.players.map((player) => (
                            <tr>
                                <td>{player.playername}</td>
                                <td>{player.playerid}</td>
                                <td></td>
                            </tr>
                        ))}
                    </tbody>
                </table> */}

                
                <PerGameTable players = {this.state.players}  sort = {this.log}/>
                
            </div>
            </SiteWrapper>
        )
    }
}

// this.props.players.map((player) =>(  
    // <Player key={player.playerid} player ={player} add={this.props.add} />   

export default PlayersPerGame

