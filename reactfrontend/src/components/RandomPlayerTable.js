import React, { Component } from 'react'
import axios from 'axios';
import {Card,colors, Grid} from 'tabler-react';
import C3Chart from 'react-c3js';
import '../c3.css'
export class RandomPlayerTable extends Component {
    state = {
        playerPerGame:[],
        playerZScores:[],
        cards: [],
    }
    componentDidMount() {
        // var url = 'http://localhost:5000/_rand_player' 
        var   url = '/_rand_player'
        axios.get(url)
        .then(res => (
            this.setState({playerPerGame: res.data.perGame, playerZScores: res.data.zScore})
            ,axios.get('/test/'+res.data.perGame.playerid)
            // ,axios.get('http://localhost:5000/test/'+res.data.perGame.playerid)
            .then(res2 => (this.setState({cards:res2.data})))
        ))
        
        }
    render() {

        return (
            <React.Fragment>
                {/* <h1>Random</h1> */}
                <div style = {{backgroundColor:'rgb(49, 245, 245,.2)',borderRadius:20,textAlign:'center'}}>
                  
                    <h1>{this.state.playerPerGame.playername}</h1>
                    <h2>Team: {this.state.playerPerGame.teamabbr}</h2>
                    <h2>Games Played: {this.state.playerPerGame.gp}</h2>
                </div>
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
                <div className = "row">
                {this.state.cards.map((chart, i) => (
            <Grid.Col key={i} md={6} xl={4}>
              <Card title={chart.title}>
                <Card.Body>
                  <C3Chart
                    data={chart.data}
                    axis={chart.axis}
                    legend={{
                      show: true, //hide legend
                    }}
                    padding={{
                      bottom: 0,
                      top: 0,
                    }}
                    colors={{
                      data1:'red'
                    }}
                  />
                </Card.Body>
              </Card>
            </Grid.Col>
          ))}
          </div>
            </React.Fragment>
        )
    }
}

export default RandomPlayerTable
