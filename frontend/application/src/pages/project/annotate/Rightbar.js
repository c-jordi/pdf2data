import React from "react"
import Panel from "./Panel"
import {RadioInput, ToggleButton, MultiLineInput} from "../../../components/inputs";
import {BiRotateRight, BiTransfer, BiArrowToLeft} from "react-icons/bi";
import "./style.scss";

const Rightbar = () => {
    return <div className="rightbar">
        <Panel title={"Quick Select"}></Panel>
        <Panel title={"Labels"}>
            <RadioInput name="labels"  options={[
                {label:<BiRotateRight/>,value:"cycle"},
                {label:<BiTransfer/>,value:"toggle"},
                {label:<BiArrowToLeft/>,value:"all"},
            ]}/>
        </Panel>
        <Panel title={"Selection modes"}>
            <RadioInput name="selection-modes"  options={[
                {label:<><div className="circle"/><span>Headline</span></>,value:"headline"},
                {label:<><div className="circle"/><span>Body</span></>,value:"body"},
            ]}/>
        </Panel>
        <Panel title={"Flag"}>
            <ToggleButton>Flag</ToggleButton>
        </Panel>
        <Panel title={"Notes"}>
            <MultiLineInput
                name="project-new-desc"
                placeholder="Enter a description"
                persist={true}
            ></MultiLineInput>
        </Panel>
    </div>
}

export default Rightbar;