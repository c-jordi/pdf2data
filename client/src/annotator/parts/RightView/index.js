import {Panel, PanelBox, Block} from "../../components/views"
import {TabInput, RadioInput, MultiLineInput, LabelInput, ClickInputs} from "../../components/inputs"
import {BiSync,BiTransfer,BiArrowToLeft, BiFlag, BiDownload} from "react-icons/bi";

const RightView = (props) => {
    const coords = {
        left : props.left,
        right : 0,
        top: 44,
        bottom: 0,
    }

    return <Panel style={coords}>
            <PanelBox>
                <TabInput value={"selection"} options={[{value:"selection", label:"Selection"},{value:"prediction", label:"Prediction"}]}></TabInput>
            </PanelBox>
            <Block title={"Shortcuts"}>
                <ClickInputs options={[
                    {label: <BiFlag/>, value:'flag' },
                    {label: <BiDownload/>, value:'download'}
                ]}></ClickInputs>
            </Block>
            <Block title={"Selection modes"}>
                <RadioInput options={[
                    {label:<BiSync/>, value:"alternate"},
                    {label:<BiTransfer/>, value:"swap"},
                    {label:<BiArrowToLeft/>, value:"toggle"},
                ]} value={"alternate"}></RadioInput>
            </Block>
            <Block title={"Labels"}>
                <LabelInput></LabelInput>
            </Block>
            
            <Block title={"Notes"} flush={true}><MultiLineInput placeholder={"Enter your notes"}></MultiLineInput></Block>
            
        </Panel>
}

export default RightView;