import React, {useReducer} from "react"
import { BiX } from "react-icons/bi";
import "./style.scss";


const TickInput = () => {

    const reducer = (state, action) => {
        switch(action){
            case "toggle":
                return !state
            default:
                return 
        }
    }

    const [isTicked, dispatch] = useReducer(reducer, false)

    const handleClick = () => {
        dispatch("toggle");
    }

    return <div className="input-tick"  onClick={handleClick} {...{"data-ticked":isTicked}}>{isTicked? <BiX/>:""}</div>
}

export default TickInput;