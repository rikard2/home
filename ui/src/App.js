import React, { Component } from 'react';
import Rule from './Rule';
import './App.css';
import { Button } from 'semantic-ui-react'

class App extends Component {
    newRule() {
        console.log('new rule');
    }
    render() {
        var rules = [];
        rules.push(<Rule key="1" name="hej">hejsan</Rule>);
        rules.push(<Rule key="2" name="whatever">whatevs</Rule>);
        return (
            <div className="ui container">
                <h2 className="ui dividing header">Rules</h2>
                {rules}
                <Button onClick={this.newRule}>New rule</Button>
            </div>
        );
    }
}

export default App;
