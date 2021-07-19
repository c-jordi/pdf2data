import React, {useReducer} from "react"
import {TickInput} from "../../inputs"
import { BiChevronDown } from "react-icons/bi";
import "./style.scss"

const ItemParent = ({data,children}) => {

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

    return <div className='item-parent'>
        <div className="item-header">
            <TickInput></TickInput>
            <div className='name' onClick={handleClick}>
                <div className='label'>{data.label}</div>
                <div className='caption'>{data.caption}</div>
            </div>
        </div>
        <div className="item-body" data-hidden={isToggled}>{children}</div>
    </div>
}

export default ItemParent;