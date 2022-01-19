import React, { Component } from 'react';
import './App.css';
import SearchUrl from './components/SearchUrl';
import AllUrls from './components/AllUrls';

document.body.style = 'background: #e7feff;';

class App extends Component{
  render() {
    const mystyle1 = {
      position: "absolute",
      top: "30%",
      marginTop: "-50px",
      width: "200px",
      height: "200px",
   };

   const mystyle2 = {
    position: "absolute",
    bottom: "30%",
    left: "75%",
    color: "#1A5276",
    fontSize: "20px",
  };
  
  return (
      <div className="App">
        <h1 style = {{color: '#3C565B'}}>SPRINT 4: User Interface for CRUD API</h1>
        <div style={mystyle1}>
          <AllUrls></AllUrls>
        </div>
        <p></p>
        <SearchUrl></SearchUrl>
        <p></p>
        <div style={mystyle2}>
          <h4>Designed by Abdullah Zaman Babar</h4>
          <p style={{fontSize: "17px"}}>Email: <a href="mailto:abdullah.zaman.babar.s@skipq.org">abdullah.zaman.babar.s@skipq.org</a></p>
        </div>
      </div>
  );
  }
}

export default App;
