import React from "react"
import PropTypes from "prop-types"
import "./style.scss";

const Panel = ({children, title}) => {
    return <div className="panel">
        <div className="title">{title}</div>
        <div className="content">{children}</div> 
        </div>
}

Panel.propTypes = {
    title : PropTypes.string
}

Panel.defaultProps = {
    title : ""
}

export default Panel