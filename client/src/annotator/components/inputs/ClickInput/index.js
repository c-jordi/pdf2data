import React, {useReducer} from "react"
import PropTypes from "prop-types"
import "./style.scss";

const ClickInput = ({style, label, value}) => {

    const reducer = (state, action) => {
        switch(action){
            case "toggle":
                return !state
            default:
                return 
        }
    }

    const [isClicked, dispatch] = useReducer(reducer, false)

    const handleClick = () => {
        dispatch("toggle");
    }

    const _className = 'd-clickinput' + (isClicked? " active":"")
    return <div className={_className} onClick={handleClick} {...{"data-ticked":isClicked}}>{label}</div>
}

export default ClickInput;

export const ClickInputs = ({style, options}) => {
    return <div className='d-clicks'>{options.map((opt)=><ClickInput style={style} label={opt.label} value={opt.value} key={opt.value}></ClickInput>)}</div>
}

ClickInputs.defaultProps = {
    options : [
        
    ]
}