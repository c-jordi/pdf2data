import React from "react";
import PropTypes from "prop-types";
import {
  Link,
} from "react-router-dom";
import "./style.scss"

const Sidebar = ({active}) => {
    return <div className='sidebar'>
        <div className='header'>pdf2data</div>
        <div className='nav'>
            <div className="header">Menu</div>
            <Link to="/" className="item">Create a project</Link>
            <Link to="/projects" className="item">Projects</Link>
        </div>
    </div>
}
Sidebar.propTypes = {
	active: PropTypes.string,
};

Sidebar.defaultProps = {
	active : "/"
};

export default Sidebar;