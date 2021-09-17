import {Panel, PanelBox, Block} from "../../components/views"
import {TabInput, FilterInput, TickInputs, SearchInput} from "../../components/inputs"

const LeftView = (props) => {
    const coords = {
        left : 0,
        right : props.right,
        top: 44,
        bottom: 0
    }
    return <Panel style={coords}>
            <PanelBox>
                <TabInput></TabInput>
            </PanelBox>
            <PanelBox>
                <Block title={"Filter"}>
                    <SearchInput></SearchInput>
                    <TickInputs labels={['Labels','Flags']}></TickInputs>
                </Block>
            </PanelBox>
        </Panel>
}

export default LeftView;