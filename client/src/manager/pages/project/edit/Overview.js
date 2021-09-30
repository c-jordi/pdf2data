import { useReducer, useEffect} from "react"
import {MultiLineInput} from "../../../components/inputs"

const Overview = (props) => {

    const reducer = (state, {name,action}) => {
        switch(action.type){
            case "overwrite":
                return {...state, name:action.value}
            default:
                return state
        }
    }

    const [state, dispatch] = useReducer(reducer, {})

    const genOnChange = (name) => {
        return (action) => {
            dispatch({name,action})
        }
    } 

    return <div className='overview'>
        <div className='section'>
            <div className='header'>Notes</div>
            <div className='caption'></div>
            <MultiLineInput value={"Some notes just for fun"} onChange={genOnChange("notes")} {...{"data-sync":"/"}}></MultiLineInput>
        </div>

    </div>
}

export default Overview;