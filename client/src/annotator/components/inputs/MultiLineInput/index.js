import PropTypes from "prop-types";

import "./style.scss";

const MultiLineInput = ({ value, onChange, placeholder, required}) => {

	const handleChange = (evt) => {
		onChange({type:"overwrite",value: evt.target.value})
	}

	const properties = {
		value,
		placeholder,
		required,
		className : "d-multiline",
		type : "text",
	}

	return (
		<textarea
			onChange={handleChange}
			{...properties}
		></textarea>
	);
};

MultiLineInput.propTypes = {
	value : PropTypes.string.isRequired,
	onChange : PropTypes.func.isRequired,
	placeholder: PropTypes.string,
	required: PropTypes.bool,
};

MultiLineInput.defaultProps = {
	placeholder: "",
	required: false,
	onChange : console.log
};


export default MultiLineInput;