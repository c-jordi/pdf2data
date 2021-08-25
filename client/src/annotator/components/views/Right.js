import Panel from "./Panel"
import {CheckboxInput, RadioInput, MultiLineInput} from "../../../../components/inputs"
import {BiRotateRight, BiTransfer, BiArrowToLeft} from "react-icons/bi";

const Right = () => {
    return <div className="right">
            <div className="border"></div>
            <div className="content">
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
                <CheckboxInput></CheckboxInput>
            </Panel>
            <Panel title={"Notes"}>
                <MultiLineInput
                    placeholder="Enter your notes"
                ></MultiLineInput>
            </Panel>
            </div>
        </div>
}

export default Right;