import React, {useReducer} from "react"
import { BiCheck } from "react-icons/bi";
import "./style.scss";


const TickInput = ({style, label}) => {

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

    return <div className='d-tick-input' onClick={handleClick}><div className="btn"  style={style} {...{"data-ticked":isTicked}} >{isTicked? <BiCheck/>:""}</div><span className="label">{label}</span></div>
}

export default TickInput;

export const TickInputs = ({style, labels}) => {
    return <div className='d-ticks'>{labels.map(label=><TickInput style={style} label={label} key={label}></TickInput>)}</div>
}