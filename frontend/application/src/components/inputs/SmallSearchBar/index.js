import PropTypes from "prop-types";
import React, { useState, useRef } from "react";
import { BiSearch } from "react-icons/bi";
import {setCachedInputValue, getCachedInputValue} from "../../../services/forms.ts"

import "./style.scss";

const SmallSearchBar = ({ name, placeholder, required, persist }) => {

	const inputRef = useRef()
	const defaultInputValue = persist? getCachedInputValue(name) : ""
	const [inputValue, setInputValue] = useState(defaultInputValue);

	const handleChange = ({ target: { value } }) => {
		setInputValue(value);
		if (persist) setCachedInputValue(name, value);
	}
	
	return <div className="small-search-bar">
		<BiSearch onClick={() => {inputRef.current.focus()}}/>
		<input
			name={name}
			ref={inputRef}
			placeholder={placeholder}
			type="text"
			value={inputValue}
			onChange={handleChange}
			required={required}
		></input>
		</div>
	
};

SmallSearchBar.propTypes = {
	name: PropTypes.string.isRequired,
	placeholder: PropTypes.string,
	required: PropTypes.bool,
	persist : PropTypes.bool
};

SmallSearchBar.defaultProps = {
	placeholder: "",
	required: false,
	persist : false
};

export default SmallSearchBar;
