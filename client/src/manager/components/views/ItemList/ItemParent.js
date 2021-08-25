import React, {useReducer} from "react"
import {TickInput} from "../../inputs"
import { Redirect } from 'react-router-dom'
import {BiAlignJustify, BiMenu, BiText } from "react-icons/bi";
import "./style.scss"

const LevelIcon = (props) => {
    switch(props.level){
        case "page":
            return <BiAlignJustify/>
        case "block":
            return <BiMenu/>
        case "textline":
            return <BiText/>
        default:
            return
    }
}

const Label = (props) => {
    return <div className='a-label' style={{backgroundColor: props.color}}>{props.name}</div>
}

const ItemParent = ({data}) => {

    const reducer = (state, action) => {
        switch (action){
            case "toggle":
                return !state;
            default:
                return state
        }
    }

	const [isToggled, dispatch] = useReducer(reducer, true);

    const handleClick = () => {
        dispatch("toggle")
    }

    const hideLongText = (text, maxLength) => {
        if (text.length >= maxLength){
            return text.slice(0, maxLength) + "..."
        }
        return text
    }

    const renderLabels = (labels) => {
        return labels.map((label,i)=> <Label {...label} key={i}></Label>)
    }
    console.log(data)
    if (!isToggled){
        return <Redirect to={`/annotate/${data.uid}`}></Redirect>
    }



    return <div className='item-parent'>
        <div className="item-header">
            <LevelIcon level={data.level}></LevelIcon>
            <div className='name' onClick={handleClick}>
                <div className='label'>{hideLongText(data.name, 30)}</div>
                <div className='caption'>{hideLongText(data.description, 30)}</div>
            </div>
            <div className="a-labels">
                {renderLabels(data.labels)}
            </div>
            <div className="author">
                {data.author}
            </div>
        </div>
        <div className="item-body" data-hidden={isToggled}>{}</div>
    </div>
}

export default ItemParent;