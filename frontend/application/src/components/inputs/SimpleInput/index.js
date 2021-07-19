import PropTypes from "prop-types";

import "./style.scss";

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
