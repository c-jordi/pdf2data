import PropTypes from "prop-types";
import "./style.scss";

const SubmitButton = ({label, onClick, disabled}) => {
	return (
		<button className="input-submit"
        type="submit"
		onClick={onClick}
		disabled={disabled}
        >{label}</button>
	);
};

SubmitButton.propTypes = {
	label : PropTypes.string,
	onClick : PropTypes.func.isRequired,
	disabled : PropTypes.bool
};

SubmitButton.defaultProps = {
	label : "Submit",
	onClick : () => console.log("Submit button was clicked!"),
	disabled : false
};

export default SubmitButton;
