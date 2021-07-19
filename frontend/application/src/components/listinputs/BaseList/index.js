import PropTypes from "prop-types";
import { Component, createRef} from "react";
import {BiPlus, BiMinus } from "react-icons/bi";

import "./style.scss";

class BaseList extends Component {

    constructor(props){
        super(props);
        this.state = {
            selected : -1
        }

        this.listRef = createRef()
        this.controlRef = createRef()
        this.listenUnselect = this.listenUnselect.bind(this);
        this.setSelected = this.setSelected.bind(this);
        this.addItem = this.addItem.bind(this)
        this.removeItem = this.removeItem.bind(this)
        this.renderItems = this.renderItems.bind(this)
        this.renderItem = this.renderItem.bind(this)
    }

    setSelected(sid){
        this.setState({selected : sid})
    }

    listenUnselect(e){
        // Skip controls buttons
        if (this.controlRef.current.contains(e.target) && this.controlRef.current !== e.target){
            return;
        }

        // Check if target is parent or sibling
        const isParent = e.target.contains(this.listRef.current)
        const isChild = this.listRef.current.contains(e.target)
        if (isParent || (!isParent && !isChild)){
            this.setSelected(-1)
        } 
    }

    addItem(){
        this.props.onChange({type:"add", value : this.createItem()})
    }

    removeItem(){
        this.props.onChange({type:"remove",value:this.state.selected})
        this.setSelected(-1)
    }

    componentDidMount(){
        document.querySelector(".App").addEventListener("click", this.listenUnselect)
    }

    componentWillUnmount(){
        document.querySelector(".App").removeEventListener("click",this.listenUnselect)
    }

    renderItems({items,selected}){
        const {setSelected, props:{onChange}} = this;

        return items.map((item,i) => {
            const onClick = () =>{
                setSelected(i)
            }
            const itemOnChange = (action) => {
                onChange({key:i,...action})
            }
            return <div className="item" key={i} onClick={onClick}{...{"data-selected": +selected === i}}>{this.renderItem(item,itemOnChange)}</div>
    })}

    // --- Methods to customize in a new class

    createItem(){
        return ""
    }

    renderItem(item, onChange){
        const handleChange = (evt) => {
            onChange({type:"replace",value:evt.target.value})
        }
        return <input type="text" className="base" value={item} onChange={handleChange}></input>
    }

    // --- 


    render () {
        const {value} = this.props;
        const {state:{selected}} = this;
        const isRemoveButtonLocked = value.length < 2 || selected === -1;

        return <div className="input-list">
        <div className="content">
            <div className="list" ref={this.listRef}>{this.renderItems({items:value,selected})}</div>
        </div>
        <div className="controls" ref={this.controlRef}>
            <div className="add" onClick={this.addItem}><BiPlus/></div>
            <div className="remove" onClick={isRemoveButtonLocked?null:this.removeItem}{...{"data-lock":isRemoveButtonLocked}}><BiMinus/></div>
        </div>
    </div>
    }
}

BaseList.propTypes = {
    value : PropTypes.array.isRequired,
    onChange : PropTypes.func.isRequired
}

BaseList.defaultProps = {
    value : [
        "this file"
    ],
    onChange : console.log,
}

export default BaseList;