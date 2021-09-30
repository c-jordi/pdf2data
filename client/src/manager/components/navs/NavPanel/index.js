import { useState } from "react"
import PropTypes from "prop-types";
import NavHorizontal from "../NavHorizontal"

const NavPanel = ({panels}) => {

    const [state, setState] = useState({selected:0})

    const menu = panels.map(({label},i) => ({label, action:()=>{setState({selected:i})}}))

    const renderPanel = (i) => {
        return panels[i].content
    }

    return <div className="panel-navigator">
        <NavHorizontal name="project-selector" className="edit-nav" menu={menu}></NavHorizontal>
        {renderPanel(state.selected)}
    </div>
}

NavPanel.propTypes = {
    panels : PropTypes.array.isRequired
}

NavPanel.defaultTypes = {
    panels : [{label: "Basic", content: <h1>Basic</h1>}]
}

export default NavPanel;