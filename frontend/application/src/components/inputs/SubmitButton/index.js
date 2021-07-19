import PropTypes from "prop-types";
import "./style.scss";

const SubmitButton = ({label, onClick}) => {

	return (
		<button className="input-submit"
        type="submit"
		onClick={onClick}
        >{label}</button>
	);
};

SubmitButton.propTypes = {
	label : PropTypes.string,
	onClick : PropTypes.func.isRequired
};

SubmitButton.defaultProps = {
	label : "Submit",
	onClick : () => console.log("Submit button was clicked!")
};

export default SubmitButton;
