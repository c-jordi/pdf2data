import React, {Component} from "react"
import { Redirect } from 'react-router-dom'
import {reduceState, reduceCallback,renderElement, validateState} from "../../components/logic"
import {saveObject, getSavedObject, clearSavedObjects} from "../../../shared/services/autosave"
import PropTypes from "prop-types"
import FormUpload from "./FormUpload";

export default class FormHandler extends Component {
    constructor(props){
        super(props);     
        
        this.state = this.verify(this.createState())
        
        this.formCallback = this.formCallback.bind(this)
        this.prefix = this.props.params.name + '-';
        this.loadSavedState = this.loadSavedState.bind(this)
        this.autosaveState = this.autosaveState.bind(this)
        this.clearSavedState = this.clearSavedState.bind(this)
        this.sendForm = this.sendForm.bind(this)   
        this.onFormSuccess =  this.onFormSuccess.bind(this)
    }

    createState(){
        const newState = this.props.content.reduce(reduceState, {_names : []});
        if (this.props.params.autosave){
            const cachedState = this.loadSavedState(this.props.params.name)
            return {...newState,...cachedState};
        }
        return newState
    }

    verify(state){
        const temp = validateState(state)
        console.log(temp)
        return temp
    }

    runMethod({origin,action}){
        switch (action.type){
            case "send":
                return this.sendForm()
            default:
                return     
        }
    }

    onFormSuccess(){
        this._redirect = true;
        this.setState({})
    }


    sendForm(){
        this.clearSavedState()
        new FormUpload(this.props.params, this.state, this.onFormSuccess).run()
    }

    loadSavedState(){
        return getSavedObject(this.props.params.name + '-');
    }

    autosaveState(){
        saveObject(this.prefix, this.state)
    }

    async clearSavedState(){
        clearSavedObjects(this.prefix)
    }

    formCallback(callObj){
        // Method callback
        if (callObj.origin.type === 'submit'){
            this.runMethod(callObj)
        }   
        // State callback
        else {
            this.setState(this.verify(reduceCallback(this.state,callObj)))
        }
    }

    renderContent(){
        const {state, formCallback} = this;
        return this.props.content.map((el) => renderElement(el,state,formCallback))
    }

    render(){
        if (this._redirect){
            return <Redirect to={this.props.params.redirect}></Redirect>
        }
        this.autosaveState()
        return <div className="form-logic" >{this.renderContent()}</div>
    }
    
}

FormHandler.propTypes = {
    params : PropTypes.exact({
        name : PropTypes.string.isRequired,
        autosave : PropTypes.bool,
        endpoint : PropTypes.string.isRequired,
        redirect : PropTypes.string
    }),
    content : PropTypes.array.isRequired
}

FormHandler.defaultProps = {
    params : {
        name : "default-form",
        autosave : true,
        endpoint : '',
        redirect : ''
    },
    content : []
}
