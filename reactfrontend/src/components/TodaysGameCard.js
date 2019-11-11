import React, { Component } from 'react'
import {Card} from 'tabler-react';
import axios from 'axios';
export class TodaysGameCard extends Component {
    state = {
        games:[],
        date: new Date(),
    }
    componentDidMount(){
        // var url = 'http://localhost:5000/_today_games'
        var url = "/_today_games"
        axios.get(url)
        .then(res =>(this.setState({games:res.data})))
            // this.setState({games:res})
    }
    getDate(){
        var date = this.state.date
        return date.getFullYear()
    }
    render() {
        console.log(this.state.games)
        return (
            <div className = "col-md-5">
            <Card>
                <Card.Header>
                    <h4>Todays Games</h4>
                    <h5 style = {{paddingLeft:10}}>{"(" + (this.state.date.getMonth()+1)+"/"+this.state.date.getDate()+"/"+this.state.date.getFullYear()+")"}</h5>
                </Card.Header>
                <Card.Body>
                    <div className="row">
                        {this.state.games.map((game) =>(
                            <div style={{paddingLeft:10, paddingBottom:10}}><h5>{game.matchup}</h5>
                            </div>
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
