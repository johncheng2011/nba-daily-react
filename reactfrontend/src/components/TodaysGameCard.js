import React, { Component } from 'react'
import {Card} from 'tabler-react';
import axios from 'axios';
export class TodaysGameCard extends Component {
    state = {
        games:[],
    }
    componentDidMount(){
        var url = 'http://localhost:5000/_today_games'
        // var url = "/_today_games"
        axios.get(url)
        .then(res =>(this.setState({games:res.data})))
            // this.setState({games:res})
    }
    render() {
        console.log(this.state.games)
        return (
            <div className = "col-md-5">
            <Card>
                <Card.Header>
                    Todays Games
                </Card.Header>
                <Card.Body>
                    <div className="row">
                        {this.state.games.map((game) =>(
                            <div style={{paddingLeft:10, paddingBottom:10}}>{game.matchup}</div>
                        ))}
                        {/* <img style={{width:25,height:25}} src = 'http://test-nba.herokuapp.com/logo192.png'/> @ <img style={{width:25,height:25}} src = 'http://test-nba.herokuapp.com/logo192.png'/> */}
                    </div>
                </Card.Body>
            </Card>
            </div>
        )
    }
}

export default TodaysGameCard
