import PropTypes from "prop-types";
import React, { useState } from "react";
import "./style.scss"

const defaultStyling = {
    version : 0
}


const NavHorizontal = ({name,menu,persist,styling,className}) => {

    const _styling = {...defaultStyling, ...styling};

	const [selectedId, setSelectedId] = useState(0)


    const generateMenu = () => {
        return menu.map((item,i) => {

            const handleMenuItemClick = () => {
                setSelectedId(i);
                item.action();
            }


            const _className = i === selectedId? "item active": "item";
            const _key = "k-" + name + "-" + i;
            
            return <div className={_className} onClick={handleMenuItemClick} key={_key} {...{
                "data-version": _styling.version
            }}>{item.label} </div>
        })
    }

    return <div className={"nav-horizontal " + className}>
        <div className="menu">
            {generateMenu()}
        </div> 
    </div>
}

NavHorizontal.propTypes = {
	name: PropTypes.string.isRequired,
    menu : PropTypes.arrayOf(PropTypes.object),
    persist : PropTypes.bool,
    styling : PropTypes.object,
    className : PropTypes.string
};

NavHorizontal.defaultProps = {
    menu : [
        {label:"All", action:()=>{console.log("All clicked")}},
        {label:"Other",action:()=>{}}
    ],
    persist : false,
    styling : {},
    className : ''
};

export default NavHorizontal