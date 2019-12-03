import React, { Component, useState } from 'react'
import axios from 'axios';
import {Card,Nav,Badge,Button,Form} from 'tabler-react';
import {Link} from 'react-router-dom';
import SiteWrapper from '../Header';
import DatePicker from 'react-datepicker';
import TypeRadio from '../TypeRadio';
import RandomPlayerTable from '../RandomPlayerTable';
import TodaysGameCard from '../TodaysGameCard';
import {TwitterTimelineEmbed} from 'react-twitter-embed';
import "tabler-react/dist/Tabler.css";
import "react-datepicker/dist/react-datepicker.css";

// export default function Home() {
//     const [startDate, setStartDate] = useState(new Date());
//     const radios = [<Form.Radio label = 'asdf' />,<Form.Radio label = 'dddsd' />]
//     console.log(startDate)
//     return (
//         <div>
//             <SiteWrapper>
            
            //      <div className= "row" style = {{paddingLeft: 11, paddingTop:10}}>
            //  <Card className = "col-md-3">
            //          <Card.Header>
            //              <h4>Pick A Date</h4>
            //          </Card.Header>
            //          <Card.Body>
            //             Select a date and find out who's playing

            //             <DatePicker showPopperArrow={false} selected={startDate} onChange={date => setStartDate(date)} />
            //             <Form.Radio label="dd"  checked/>
            //             <Form.SelectGroup children = {radios}/>
                        // <Button style={{margin:10}} pill color='primary'>Submit</Button>
            //          </Card.Body>
                    
            //      </Card>
//                  <Card className = "col-md-4">
//                      <Card.Header>
//                          fdsf
//                      </Card.Header>
                    
//                  </Card>
//                  </div>
//              </SiteWrapper>
             
//                <Link to="/about">about</Link>
//                <Badge color="primary" className="mr-1">
//                  primary
//                </Badge>
//                <h1>hello </h1>
//         </div>
//     )
// }


export class Home extends Component {
    state = {
        date: new Date(),
        type: 'perGame',
        player: [],

    };
    

    setStartDate = (date) =>{
        this.setState({state: date})
    };
    setType(event) {
        console.log(event.target.value)
        this.setState({type:event.target.value})
    };
    checkPerGame(){

        if(this.state.type === 'perGame'){
            
            return true
        }
    }
    getDateURL(){
        var MyDate = this.state.date
        var MyDateString = MyDate.getFullYear() + '-' + ('0' + (MyDate.getMonth()+1)).slice(-2) + '-'
             + ('0' + MyDate.getDate()).slice(-2);
        // var month = '' + date.getMonth();
        // var day = '' + date.getDate();
        // var year = '' + date.getFullYear();
        return MyDateString
    }
    getTypeURL(){
        if(this.state.type === 'perGame'){
            return 'players'
        }
        else{
            return 'zscores'
        }
    }
    
    render() {
        return (
            <div>
            <SiteWrapper>
                <div className= "row" style = {{paddingLeft: 11, paddingTop:10}}>
            <Card className = "col-md-3">
                    <Card.Header>
                        <h4>Pick A Date</h4>
                    </Card.Header>
                    <Card.Body>
                        select a date and see whos playing
                        <DatePicker selected={this.state.date} onChange={date => this.setState({date:date})} />
                        {/* <TypeRadio setType = {this.setType}/> */}
                        <div >
                            <input type="radio" value="perGame" name="type"  onChange={this.setType.bind(this)}/> Per Game
                            <input type="radio" value="ZScores" name="type"  onChange={this.setType.bind(this)}/> Z Scores
                        </div>
                        <Link to={'/'+this.getTypeURL()+'/'+this.getDateURL()}>
                        <Button style={{margin:10}} pill color='primary' to="/">Submit</Button></Link>
                    </Card.Body>
                    
                </Card>
                <TwitterTimelineEmbed
  sourceType="profile"
  screenName="WebEmbiid"
  options={{height: 400}}
/>
                <Card className = "col-md-4">
                    <Card.Header>
                        About
                    </Card.Header>
                    <Card.Body>
                        WIP
                    </Card.Body>                    
                </Card>
                <TodaysGameCard/>
                </div>
                <div className = "row" style = {{paddingLeft: 11, paddingTop:10}}>
                <RandomPlayerTable />
                </div>
            </SiteWrapper>
              <Link to="/about">about</Link>
              <Badge color="primary" className="mr-1">
                primary
              </Badge>
              <h1>hello </h1>
            
            </div>
        )
    }
}

export default Home
