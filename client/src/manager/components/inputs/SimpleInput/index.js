import PropTypes from "prop-types";
import {useState} from "react";

import "./style.scss";

const InputRequired = (props) => {
	return <div className="input-notrequired"></div>
}

const InputErrors = ({_validation = {}}) => {
	const { is_valid, errors} = _validation;
	const msgDuration = 3000;
	const [clickTime, setClickTime] = useState(new Date().getTime() - msgDuration * 2)

	if (is_valid) return <div className='input-errors-none'></div>

	const handleClick = () => {
		setClickTime(new Date().getTime());
	}


	const renderMsg = (clickTime) => {
		const delta = new Date().getTime() - clickTime;
		if (delta < msgDuration){
			setTimeout(()=>{setClickTime(new Date().getTime() - msgDuration * 2)}, msgDuration - delta)
			return <div className="input-errors-msg">{errors[0]}</div>
		}
		return <div className="input-errors-nomsg"></div>
	}

	return <>
	<div className="input-errors-icon" onClick={handleClick}>!</div>
	 {renderMsg(clickTime)}
	</>
}

const InputSuggestions = ({options, onChange}) => {

	if (options.length === 0){
		return <div className="input-nosuggestions"/>
	}

	const handleClick = (sug) => {
		return () => onChange({type:"overwrite", value:sug})
	}

	const renderSuggestions = (sugs) => {
		return sugs.map((sug) => <div className="input-suggestion" key={sug} onClick={handleClick(sug)}>{sug}</div>)
	}

	return <div className="input-suggestions">
		{renderSuggestions(options)}
	</div>

}

const SimpleInput = ({ value, onChange, placeholder, isExtended, required}) => {

	const handleChange = (evt) => {
		onChange({type:"overwrite", value: evt.target.value})
	}

	const properties = {
		placeholder,
		type : "text",
		value,
		onChange: handleChange,
		className : "input-simple",
		required,
		autoComplete: "off",
		"data-extended" : isExtended
	}

	return (
		<input
		{...properties}
		></input>
	);
};


const InputContainer = (props) => {

	const isExtended = props.suggestions.length > 0;

	return (
		<div className="input-simple-container">
			<SimpleInput isExtended={isExtended} {...props}></SimpleInput> 
			<InputSuggestions {...props}></InputSuggestions>
			<InputErrors {...props}></InputErrors>
		</div>	
	);
};

InputContainer.propTypes = {
	suggestions : PropTypes.arrayOf(PropTypes.string),
}

InputContainer.defaultProps = {
	suggestions : []
}

InputSuggestions.propTypes = {
	options : PropTypes.arrayOf(PropTypes.string),
}

InputSuggestions.defaultProps = {
	options : [],
}

SimpleInput.propTypes = {
	value : PropTypes.string.isRequired,
	onChange : PropTypes.func.isRequired,
	placeholder: PropTypes.string,
	required: PropTypes.bool,
	isExtended: PropTypes.bool
};

SimpleInput.defaultProps = {
	placeholder: "",
	required: false,
	isExtended : false
};


export default InputContainer;
