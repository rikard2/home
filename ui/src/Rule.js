import React, { Component } from 'react';

class Rule extends Component {
    render() {
        return (
            <div className="ui segment">{this.props.children}?</div>
        );
    }
}

export default Rule;
