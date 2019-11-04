import React, { Component } from 'react'
import axios from 'axios';
import ZScoresTable from '../ZScoresTable';
import SiteWrapper from '../Header';

export class PlayersZScores extends Component {
    state = {
        players: [],
    }
    log = (attr)=>{
        this.setState({players: this.state.players.sort(function(a,b) {
            var x = a[attr];
            var y = b[attr];
            return ((x < y) ? 1 : ((x > y) ? -1 : 0));

        }) })
    }
    componentDidMount() {
        // var   url = 'http://localhost:5000/_zscores/' + this.props.match.params.date;
        // var url = 'http://localhost:5000/_allPerGame'
        var   url = '/_zscores/' + this.props.match.params.date;
        axios.get(url)
        // axios.get('/_allPlayerPerGame')
        .then(res => this.setState({players: res.data}))
        }
    render() {
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

                
                <ZScoresTable players = {this.state.players}  sort = {this.log}/>
                
            </div>
            </SiteWrapper>
        )
    }
}

export default PlayersZScores
