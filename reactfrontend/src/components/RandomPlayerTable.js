import React, { Component } from 'react'
import axios from 'axios';
export class RandomPlayerTable extends Component {
    state = {
        playerPerGame:[],
        playerZScores:[],
    }
    componentDidMount() {
        var url = 'http://localhost:5000/_rand_player' 
        // var url = 'http://localhost:5000/_allPerGame'
        // var   url = '/_rand_player'
        axios.get(url)
        // axios.get('/_allPlayerPerGame')
        .then(res => (
            this.setState({playerPerGame: res.data.perGame, playerZScores: res.data.zScore})
        ))
        // this.setState({player: res.data})
        }
    render() {

        return (
            <React.Fragment>
                <h1>{this.state.playerPerGame.playername}</h1>
                <h3>{this.state.playerPerGame.teamabbr}</h3>
                <table className = "table">
                    <thead>
                        <tr>
                            <th></th>
                            <th>Field Goal Percentage</th>
                            <th>Free Throw Percentage</th>
                            <th>3 Pointers Made</th>
                            <th>Rebounds</th>
                            <th>Assists</th>
                            <th>Steals</th>
                            <th>Blocks</th>
                            <th>Points</th>
                            <th>Turnovers</th>
                            <th>Total</th>
                        </tr>
                    </thead>
                        <tr>
                            <td>Per Game Stats</td>
                            <td>{this.state.playerPerGame.fg_pct}</td>
                            <td>{this.state.playerPerGame.ft_pct}</td>
                            <td>{this.state.playerPerGame.fg3m}</td>
                            <td>{this.state.playerPerGame.treb}</td>
                            <td>{this.state.playerPerGame.ast}</td>
                            <td>{this.state.playerPerGame.stl}</td>
                            <td>{this.state.playerPerGame.blk}</td>
                            <td>{this.state.playerPerGame.pts}</td>
                            <td>{this.state.playerPerGame.tov}</td>


                        </tr>
                        <tr>
                            <td>Z Scores</td>
                            <td>{this.state.playerZScores.fgz}</td>
                            <td>{this.state.playerZScores.ftz}</td>
                            <td>{this.state.playerZScores.fg3z}</td>
                            <td>{this.state.playerZScores.rebz}</td>
                            <td>{this.state.playerZScores.astz}</td>
                            <td>{this.state.playerZScores.stlz}</td>
                            <td>{this.state.playerZScores.blkz}</td>
                            <td>{this.state.playerZScores.ptsz}</td>
                            <td>{this.state.playerZScores.tovz}</td>
                            <td>{this.state.playerZScores.total}</td>
                        </tr>
                    <tbody>
                        
                    </tbody>
                    
                </table>
            </React.Fragment>
        )
    }
}

export default RandomPlayerTable
