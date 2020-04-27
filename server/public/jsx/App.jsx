import React, { Component } from "react";
import ReactDOM from "react-dom";
import LoginCard from "./LoginCard.jsx";
import ShowPhoto from "./ShowPhoto.jsx";
import axios from "axios";

import "../css/style.scss"
class MainContainer extends Component {
    constructor() {
      super();
      this.state = {
        login: {
          id: '',
          datetime: ''
        },
        isLoggedIn: false,
        defaultphoto: 'https://previews.123rf.com/images/isselee/isselee1103/isselee110300446/8972925-british-shorthair-cat-8-months-old-in-front-of-white-background.jpg',
        photo: 'https://previews.123rf.com/images/isselee/isselee1103/isselee110300446/8972925-british-shorthair-cat-8-months-old-in-front-of-white-background.jpg',
        code: ''
      };
    };
    loginHandler = async() => {
      this.setState({isLoggedIn: !this.state.isLoggedIn});
      const response = await axios.post(
        'http://127.0.0.1:8000/hash-generator',
        {
          event_id: this.state.login.id,
          time: this.state.login.datetime
        },
        { headers: { 'Content-Type': 'application/json' } }
      )
      console.log(response.data.result)
      try{
        const photoResponse = await axios.get(`http://127.0.0.1:8000/img/${response.data.result}.jpg`);
        console.log(photoResponse)
        this.setState({photo: `img/${response.data.result}.jpg`});
        this.setState({code: response.data.result});
      }catch(err){
        alert("no photo founds");
        this.setState({photo: this.state.defaultphoto});
      }
    };
    deleteHandler = async() => {
      try{
        const response = await axios.post(
          'http://127.0.0.1:8000/delete-photo',
          {
            code: this.state.code
          },
          { headers: { 'Content-Type': 'application/json' } }
        )
        console.log(response.data.result)
      }catch(err){
        alert("no photo to remove, please try again!");
      }
      this.setState({
        code: '',
        photo: this.state.defaultphoto,
        isLoggedIn: !this.state.isLoggedIn,
        login:{id: '', datetime: ''}
      });
    };
    gobackHandler = () => {
      this.setState({
        code: '',
        photo: this.state.defaultphoto,
        isLoggedIn: !this.state.isLoggedIn,
        login:{id: '', datetime: ''}
      });
    };
    changeParentData = (inputObject) => {
      console.log(inputObject)
      for (let [key, value] of Object.entries(inputObject)) {
        this.setState({login:{...this.state.login, [key]: value}})
      }
    };
    display = () => {
      if (!this.state.isLoggedIn)
        return <LoginCard 
                handler={this.loginHandler} 
                changeParentData={this.changeParentData}
                login={this.state.login}/>
      else return <ShowPhoto photo={this.state.photo} handler={this.gobackHandler}
                  deleteHandler={this.deleteHandler}/>
    };
    render() {
      return (
        <div>
          {this.display()}
        </div>
      );
    }
}
ReactDOM.render(<MainContainer/>, document.getElementById("app"));