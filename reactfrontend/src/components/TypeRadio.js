import React, { Component } from 'react'

export class TypeRadio extends Component {
    updateCategory = (e) => {
        if(e.target.checked) {
           this.props.updateCategory(e.target.value)
        }
    }
    render() {
        return (
            <div onChange={this.updateCategory}>
                <input type="radio" value="PerGame" name="type" /> Per Game{' '}
                <input type="radio" value="ZScores" name="type"/> Z Scores
            </div>
        )
    }
}

export default TypeRadio
