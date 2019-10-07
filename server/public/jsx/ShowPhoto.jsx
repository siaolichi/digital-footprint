import React, { Component } from "react";
import Button from '@material/react-button';

import '@material/react-button/dist/button.css';

class ShowPhoto extends Component {
    constructor(){
        super();
        this.state = {
            id: '',
            datetime: ''
        }
    };
    render(){
        return(
            <div className="flex-parent-center-column">
                <img 
                    style={{width: "50%"}}
                    src={this.props.photo}
                />
                <br/>
                <Button
                    onClick={(e)=>{
                        this.props.handler();
                    }}
                >
                    back
                </Button>
            </div>
        )
    }

}

export default ShowPhoto;