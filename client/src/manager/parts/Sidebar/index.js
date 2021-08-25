import React from "react";
import PropTypes from "prop-types";
import {
  Link,
} from "react-router-dom";
import "./style.scss"

const Sidebar = ({active}) => {
    return <div className='sidebar'>
        <div className='sidebar__header'>pdf2data</div>
        <div className='nav'>
            <div className="nav__header">Recent</div>
            <div className="nav__item">Project 0</div>
            <div className="nav__header">Menu</div>
            <Link to="/" className="nav__item">Create a project</Link>
            <Link to="/projects" className="nav__item">Projects</Link>
            <Link to="/settings" className="nav__item">Settings</Link>
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