import PropTypes from "prop-types";
import "./style.scss";

const RadioInput = ({value, onChange, options, required}) => {
    const formatBox = (info) => {

        const isActive = info.value === value;
        const handleClick = () => {
            if (!isActive) onChange({type:"overwrite",value:info.value});
        }
        const className = "d-radio-box" + (isActive? " active" : "");
        return <div className={className} key={info.value} onClick={handleClick}>{info.label}</div>
    }

    const generateBoxes = (opts) => {
        return opts.map(formatBox)
    }

    return <div className="d-radio">
        {generateBoxes(options)}
    </div>
}


RadioInput.propTypes = {
    value : PropTypes.string.isRequired,
    onChange : PropTypes.func.isRequired,
	options : PropTypes.arrayOf(PropTypes.shape({
        label: PropTypes.object,
        value : PropTypes.string
      })),
	required: PropTypes.bool,
};

RadioInput.defaultProps = {
	options : [
        {label: 'Option 1', value: 'option1', icon : ""},
        {label: 'Option 2', value: 'option2', icon : ""},
    ],
	required: false,
    onChange : (log) => {console.log(log)}
};


export default RadioInput;