import React, {Component} from "react"
import {reduceState, reduceCallback,renderElement} from "../../components/logic"
import PropTypes from "prop-types"

export default class FormHandler extends Component {
    constructor(props){
        super(props);
        
        this.state = this.createState()

        this.formCallback = this.formCallback.bind(this)

        console.log(this.props, this.state)
    }

    createState(){
        const newState = this.props.content.reduce(reduceState, {_names : []});
        if (this.props.caching){
            const cachedState = this.loadCachedState(this.props.fid)
            return {...newState,...cachedState};
        }
        return newState
    }

    runMethod(callObj){

    }

    loadCachedState(){

    }

    cachedState(){

    }

    formCallback(callObj){

        // Method callback
        if (callObj.origin.method){
            this.runMethod(callObj)
        }   
        // State callback
        else {
            this.setState(reduceCallback(this.state,callObj))
        }
        
    }

    renderContent(){
        const {state, formCallback} = this;
        return this.props.content.map((el) => renderElement(el,state,formCallback))
    }

    render(){
        console.log(this.state)
        return <div className="form-logic" >{this.renderContent()}</div>
    }
    
}


