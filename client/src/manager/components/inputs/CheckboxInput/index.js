import PropTypes from "prop-types";
import "./style.scss";

const CheckboxInput = (props) => {
    return <button className='simple-button' {...props}>
        {props.children}
    </button>
}


CheckboxInput.propTypes = {
    value : PropTypes.string.isRequired,
    onChange : PropTypes.func.isRequired,
	options : PropTypes.arrayOf(PropTypes.shape({
        label: PropTypes.object,
        value : PropTypes.string
      })),
	required: PropTypes.bool,
};

CheckboxInput.defaultProps = {
	options : [
        {label: 'Option 1', value: 'option1', icon : ""},
        {label: 'Option 2', value: 'option2', icon : ""},
    ],
	required: false,
    onChange : console.log
};



export default CheckboxInput;