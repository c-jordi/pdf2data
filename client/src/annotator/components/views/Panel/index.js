import {useState} from "react";
import PropTypes from "prop-types"
import "./style.scss";

export const Panel = ({children, style}) => { 
    return <div className="panel" style={style} >{children}</div>
}

export const PanelBox= ({children}) => {
    return <div className="panel-box">{children}</div>
}

Panel.propTypes = {
    orient : PropTypes.bool,
    style : PropTypes.object
}

Panel.defaultProps = {
    orient : false,
    style : {}
}
