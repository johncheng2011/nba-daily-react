import React, { Component } from 'react'

export class TypeRadio extends Component {

    render() {
        return (
            <div onChange={this.props.setType.bind(this)}>
                <input type="radio" value="PerGame" name="type" /> Per Game{' '}
                <input type="radio" value="ZScores" name="type"/> Z Scores
            </div>
        )
    }
}

export default TypeRadio
