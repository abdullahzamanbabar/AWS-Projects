import React, { Component } from 'react';
import axios from 'axios';

class SearchUrl extends Component {
    constructor(props) {
        super(props);

        this.state = {
            value : '',
            result : '',
        }
    }
        
    getValue = (event) => { // it raises event on every letter entered so we want the last event which is the complete word
        this.setState({value : event.target.value});
    };

    clickHandler2 = () => { //On click we store the last event in a variable
        const value = this.state.value; 
        console.log(value)
        axios.get('https://l2qs966u0c.execute-api.us-east-2.amazonaws.com/prod/url?URL_ADDRESS='+value)
        .then((response) => {
            this.setState({result: 'The Url '+value+' Exists in the DataBase'});
            //console.log(this.state.result)
        })
        .catch((error) => {
            this.setState({result: value+' NOT FOUND'});
            //console.log(this.state.result)
        })
    };

    render() {
        return (
            <div>
                <input type="text" onChange={this.getValue}/>
                <button onClick={this.clickHandler2}>Search URL</button>
                {
                    <h1 style={{color: '#CD5C5C'}}>{this.state.result}</h1>
                }
            </div>
        );
    }
}
SearchUrl.propTypes = {

};

export default SearchUrl;