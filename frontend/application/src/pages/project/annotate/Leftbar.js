import React, {useReducer} from "react";
import {SmallTickInput} from "../../../components/inputs"
import {NavHorizontal} from "../../../components/navs"
import "./style.scss";


const Filtering = () => {
    return <div className="filtering">
        <div className="query">
        </div>
        <div className="parameters">
            <SmallTickInput label={"Labels"}></SmallTickInput>
            <SmallTickInput label={"Names"}></SmallTickInput>
            <SmallTickInput label={"Flagged"}></SmallTickInput>
        </div>
    </div>
}

const Leftbar = () => {

    // This should be changed. The state is stored twice. It should always kept in the parent component
    const reducer = (action, state) => {
        switch (action.type){
            case "set_type":
                console.log("setting type:",action.value)
                return {...state, type : action.value}
            case "set_filter":
                return {...state, filter : {[action.name] : action.value}}
            default:
                return {...state}
        }
    }

    const [selection, setSelection] = useReducer(reducer, {
        state : "random",
        properties : {}
    })

    const showOptions = (obj) => {
        if (obj.type === "filtered"){
            return <div className="options">
            <Filtering></Filtering>
        </div>
        }
        else {
            return <></>
        }
    }

    return <div className="leftbar">
        <div className="selection">
            <div className="type">
                <NavHorizontal name="annotate-case-selection" menu={[
                    {label:"Random", action:() => {setSelection({type:"set_type",value:"random"})}},
                    {label:"All", action:()=> {setSelection({type:"set_type",value:"all"})}},
                    {label:"Filtered", action:()=> {setSelection({type:"set_type",value:"filtered"})}},
                ]} styling={{version : 1 }}></NavHorizontal>
            </div>
            {showOptions(selection)}
        </div>
        

    </div>
}

export default Leftbar;