import React, { Component } from 'react'


export class Player extends Component {
    add = (e) =>{
        console.log(this.props.player.ast)

    }


    render() {
        //console.log(this.props)
        return (
            <div>
                <input type='button' onClick={this.props.add.bind(this,this.props.player.playerid)}/>
                {this.props.player.ast}
            </div>
        )
    }
}


export default Player
