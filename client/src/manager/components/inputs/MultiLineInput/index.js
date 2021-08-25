import PropTypes from "prop-types";

import "./style.scss";

const InputContainer = (props) => {
	return <div className='input-container'>
		<MultiLineInput {...props}></MultiLineInput>
	</div>
}

const MultiLineInput = ({ value, onChange, placeholder, required}) => {

	const handleChange = (evt) => {
		onChange({type:"overwrite",value: evt.target.value})
	}

	const properties = {
		value,
		placeholder,
		required,
		className : "input-multiline",
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
};

export default InputContainer;
