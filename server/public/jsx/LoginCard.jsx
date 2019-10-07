import React, { Component } from "react";
import TextField, {HelperText, Input} from '@material/react-text-field';
import Button from '@material/react-button';

import '@material/react-text-field/dist/text-field.css';
import '@material/react-button/dist/button.css';

class LoginCard extends Component {
    constructor(props){
        super();
        console.log(props)
    };
    render(){
        return(
            <div className="flex-parent-center-column">
                <TextField
                    name="id"
                    label="Event ID"
                    helperText={<HelperText>Please fill the event ID</HelperText>}
                >
                    <Input
                        value={this.props.login.id} 
                        onChange={(e) => this.props.changeParentData({id: e.currentTarget.value})} 
                        />
                </TextField>
                <TextField
                    name="datetime"
                    label="Date and Time"
                    helperText={<HelperText>Please fill the event's date and time</HelperText>}
                >
                    <Input
                        value={this.props.login.datetime} 
                        onChange={(e) => this.props.changeParentData({datetime: e.currentTarget.value})} 
                        />
                </TextField>
                <Button
                    onClick={(e)=>{
                        this.props.handler();
                    }}
                >
                    Submit
                </Button>
            </div>
        )
    }

}

export default LoginCard;