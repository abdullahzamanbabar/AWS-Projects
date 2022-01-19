import React, { Component } from 'react';
import axios from 'axios';
import ReactPaginate from 'react-paginate';

class ClassClick extends Component {

    constructor(props){
        super(props);

        this.state = {
            posts: [],
        };
    }

    clickHandler1 = () => {
        axios.get('https://l2qs966u0c.execute-api.us-east-2.amazonaws.com/prod/urls?_limit=3')
        .then((response) => {
            console.log(response.data)
            this.setState({posts: response.data});
        })
        .catch((error) => {
            console.log(error)
        })
    }

    render() {

        const mystyle = {
            //border: "3px solid black",
            //height: "30px",
           // align: "center",
            //width: "200px",
            //position: "relative",
            //padding: "10px",
            //borderBottom: "3px solid black",
          };
         const mystyle1 = {
            position: "absolute",
            top: "30%",
            //left: "50%",
            marginTop: "-50px",
            //marginLeft: "-50px",
            width: "100px",
            height: "100px",
         };

        const {posts} = this.state
        return (
        <div>
            <button onClick={this.clickHandler1}>GET URLs</button>
            <div style={mystyle1}>
            <ol>
            {
                posts.length ?
                posts.map(post =>
                    <li style={{padding: "10px"}}><a href={"https://"+post.URL_ADDRESS}>{post.URL_ADDRESS}</a></li>
                    ) :
                null
            }
            </ol>
            </div>
        </div>
        );
    }
}
      
export default ClassClick;