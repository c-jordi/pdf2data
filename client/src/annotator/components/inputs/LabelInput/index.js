import PropTypes from "prop-types";
import "./style.scss";

const LabelInput = ({options, value, onChange}) => {

    const formatLabel = (opt) => {
        const isActive = opt.value === value;
        const handleClick = () => {
            if (!isActive) onChange({type:"overwrite",value:opt.value});
        }
        const _className = "label" + (isActive? " active":"");
        return <div className={_className} onClick={handleClick}><div className='ind'style={{backgroundColor: opt.color}} />{opt.label}</div>
    }

    const generateLabels = (opts) => {
        return opts.map(formatLabel)
    }

    return <div className='d-labelinput'>{generateLabels(options)}</div>
}


LabelInput.defaultProps = {
    options : [
        {label: "Headline", color : "purple", value: "headline"},
        {label: "Description", color: "green", value: "description"},
        {label: "Footer", color: "orange", value: "footer"},
        {label: "None", color: "grey", value: "none"}
    ],
    onChange : console.log,
    value: "headline"
}

export default LabelInput;