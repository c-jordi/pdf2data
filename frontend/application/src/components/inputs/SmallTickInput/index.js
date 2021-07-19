import React, {useReducer} from "react"
import PropTypes from "prop-types";
import { BiCheck } from "react-icons/bi";
import "./style.scss";


const SmallTickInput = ({label}) => {

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

    return <div className="small-input-tick" onClick={handleClick} {...{"data-ticked":isTicked}}> <div className="tick">{isTicked? <BiCheck/>:""} </div> <div className="label">{label}</div></div>
}

SmallTickInput.propTypes = {
	label: PropTypes.string
};

SmallTickInput.defaultProps = {
	label : ""
};




export default SmallTickInput;