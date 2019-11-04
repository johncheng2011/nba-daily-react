import React, { Component } from 'react'


export class PerGameTable extends Component {
    state = {
        sorted: 'pts',

    }
    counter = () =>{
        
        return this.state.counter
    }
    stuff = (i) =>{
        var t = i % 10
        if(t ===0 && i!== 0){ 
        return(
            <tr>
                <th>count</th>
                <th>Player Name </th>
                <th style = {this.bolden('teamabbr')}>Team</th>
                <th style = {this.bolden('gp')}>GP </th>
                <th style = {this.bolden('min')}>Min</th>
                <th style = {this.bolden('fg_pct')}>FG%</th>
                <th style = {this.bolden('fg3m')}>FG3m</th>
                <th style = {this.bolden('ft_pct')}>FT%</th>
                <th style = {this.bolden('treb')}>TReb</th>
                <th style = {this.bolden('ast')}>Ast</th>
                <th style = {this.bolden('stl')}>Stl</th>
                <th style = {this.bolden('blk')}>Blk</th>
                <th style = {this.bolden('pts')}>Pts</th>
                <th style = {this.bolden('tov')}>Tov</th>
                <th style = {this.bolden('foul')}>Foul</th>
            </tr>
        )}
    }
    bolden = (column) =>{
        if(this.state.sorted === column){
            return {fontWeight: "bold", fontSize: "115%",cursor:'pointer'}
        }
        return {cursor:'pointer'}
    }
    


    clickHeader = (header) =>{
        this.props.sort(header)
        this.setState({sorted: header})
    }

    render() {
        return (
            <table className = 'table'>
                <thead>
                    <tr>
                        <th>count</th>
                        {/* {this.props.sort.bind(this,'playername')} */}
                        {/* {this.props.sort.bind(this,'teamabbr')} */}
                        <th>Player Name</th>
                        <th onClick = {this.clickHeader.bind(this,'teamabbr')} style = {this.bolden('teamabbr')}>Team</th>
                        <th onClick = {this.clickHeader.bind(this,'gp')} style = {this.bolden('gp')}>GP</th>
                        <th onClick = {this.clickHeader.bind(this,'min')} style = {this.bolden('min')}>Min</th>
                        <th onClick = {this.clickHeader.bind(this,'fg_pct')} style = {this.bolden('fg_pct')}>FG%</th>
                        <th onClick = {this.clickHeader.bind(this,'fg3m')} style = {this.bolden('fg3m')}>FG3m</th>
                        <th onClick = {this.clickHeader.bind(this,'ft_pct')} style = {this.bolden('ft_pct')}>FT%</th>
                        <th onClick = {this.clickHeader.bind(this,'treb')} style = {this.bolden('treb')}>TReb</th>
                        <th onClick = {this.clickHeader.bind(this,'ast')} style = {this.bolden('ast')}>Ast</th>
                        <th onClick = {this.clickHeader.bind(this,'stl')} style = {this.bolden('stl')}>Stl</th>
                        <th onClick = {this.clickHeader.bind(this,'blk')} style = {this.bolden('blk')}>Blk</th>
                        <th onClick = {this.clickHeader.bind(this,'pts')} style = {this.bolden('pts')}>Pts</th>
                        <th onClick = {this.clickHeader.bind(this,'tov')} style = {this.bolden('tov')}>Tov</th>
                        <th onClick = {this.clickHeader.bind(this,'fouls')} style = {this.bolden('fouls')}>Foul</th>
        
                        
                    </tr>
                </thead>
                <tbody>
                    {this.props.players.map((player,i) => (
                                <React.Fragment>
                                {this.stuff(i)}       
                                <tr>
                                    <td>{i+1}</td>
                                    <td>{player.playername}</td>
                                    <td>{player.teamabbr}</td>
                                    <td>{player.gp}</td>
                                    <td>{player.min}</td>
                                    <td>{player.fg_pct}</td>
                                    <td>{player.fg3m}</td>
                                    <td>{player.ft_pct}</td>
                                    <td>{player.treb}</td>
                                    <td>{player.ast}</td>
                                    <td>{player.stl}</td>
                                    <td>{player.blk}</td>
                                    <td>{player.pts}</td>
                                    <td>{player.tov}</td>
                                    <td>{player.fouls}</td>



                                </tr>
                                </React.Fragment>
                    ))}
                </tbody>
            </table>
        )
    }
}


export default PerGameTable


// ast: 0.8
// blk: 0
// dreb: 1.5
// fg3_pct: 0.077
// fg3a: 3.3
// fg3m: 0.3
// fg_pct: 0.333
// fga: 4.5
// fgm: 1.5
// fouls: 0.5
// ft_pct: 0
// fta: 0
// ftm: 0
// gp: 4
// loss: 2
// min: 12.8
// oreb: 0
// playerid: 1713
// playername: "Vince Carter"
// pts: 3.3
// stl: 0.5
// teamabbr: "ATL"
// teamid: 1610612737
// tov: 0.5
// treb: 1.5
// win: 2