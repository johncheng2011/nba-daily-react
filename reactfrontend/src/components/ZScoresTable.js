import React, { Component } from 'react'

export class ZScoresTable extends Component {
    state = {
        sorted: 'total',
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
                <th style = {this.bolden('fgz')}>FG Z</th>
                <th style = {this.bolden('ftz')}>FT Z</th>
                <th style = {this.bolden('fg3mz')}>FG3 Z</th>
                <th style = {this.bolden('rebz')}>Reb Z</th>
                <th style = {this.bolden('astz')}>Ast Z</th>
                <th style = {this.bolden('stlz')}>Stl Z</th>
                <th style = {this.bolden('blkz')}>Blk Z</th>
                <th style = {this.bolden('ptsz')}>Pts Z</th>
                <th style = {this.bolden('tovz')}>Tov Z</th>
                <th style = {this.bolden('total')}>Total</th>
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
                        <th>Count</th>
                        <th>Player Name</th>
                        <th onClick = {this.clickHeader.bind(this,'teamabbr')} style = {this.bolden('teamabbr')}>Team</th>
                        <th onClick = {this.clickHeader.bind(this,'gp')} style = {this.bolden('gp')}>GP</th>
                        <th onClick = {this.clickHeader.bind(this,'min')} style = {this.bolden('min')}>Min</th>
                        <th onClick = {this.clickHeader.bind(this,'fgz')} style = {this.bolden('fgz')}>FG Z</th>
                        <th onClick = {this.clickHeader.bind(this,'ftz')} style = {this.bolden('ftz')}>FT Z</th>
                        <th onClick = {this.clickHeader.bind(this,'fg3z')} style = {this.bolden('fg3z')}>FG3 Z</th>
                        <th onClick = {this.clickHeader.bind(this,'rebz')} style = {this.bolden('rebz')}>Reb Z</th>
                        <th onClick = {this.clickHeader.bind(this,'astz')} style = {this.bolden('astz')}>Ast Z</th>
                        <th onClick = {this.clickHeader.bind(this,'stlz')} style = {this.bolden('stlz')}>Stl Z</th>
                        <th onClick = {this.clickHeader.bind(this,'blkz')} style = {this.bolden('blkz')}>Blk Z</th>
                        <th onClick = {this.clickHeader.bind(this,'ptsz')} style = {this.bolden('ptsz')}>Pts Z</th>
                        <th onClick = {this.clickHeader.bind(this,'tovz')} style = {this.bolden('tovz')}>Tov Z</th>
                        <th onClick = {this.clickHeader.bind(this,'total')} style = {this.bolden('total')}>Total</th>
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
                            <td>{player.fgz}</td>
                            <td>{player.ftz}</td>
                            <td>{player.fg3z}</td>
                            <td>{player.rebz}</td>
                            <td>{player.astz}</td>
                            <td>{player.stlz}</td>
                            <td>{player.blkz}</td>
                            <td>{player.ptsz}</td>
                            <td>{player.tovz}</td>
                            <td>{player.total}</td>



                        </tr>
                        </React.Fragment>
                    ))}
                </tbody>
            </table>
        )
    }
}

export default ZScoresTable
