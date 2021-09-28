import PropTypes from "prop-types";
import {useState, useEffect} from "react";

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

const ClickListener = ({callback}) => {
	useEffect(()=>{
		document.body.addEventListener("click", callback)

		return () => {
			document.body.removeEventListener("click", callback)
		}
	}, [callback])

	return <div className="click-listener"></div>
}

const InputSuggestions = ({options, show, onChange, setFocused}) => {

	const renderSuggestions = (sugs) => {
		return sugs.map((sug, i) => <div className="input-suggestion" key={"sug-"+i} onClick={sug.action}>{sug.content}</div>)
	}

	const onBlur = (evt) => {
		let match = false;
		let node = evt.target;
		if (!node) return;
		while(!match){
			if (node.className === "input-simple-container"){
				match = true;
			}
			else if (node.className === "App"){
				setFocused(false)
				return;
			}
			else {
				node = node.parentNode;
				if (!node) return;
			}
		}		
	}

	if (options.length === 0 || !show){
		return <div className="input-nosuggestions"/>
	}

	return <div className="input-suggestions">
		<ClickListener callback={onBlur}></ClickListener>
		{renderSuggestions(options)}
	</div>

}


const SimpleInput = ({ value, onChange, setFocused, placeholder, isExtended, required}) => {

	const handleChange = (evt) => {
		onChange({type:"overwrite", value: evt.target.value})
	}

	const onFocus = ()=>{
		setFocused(true)
	}

	const properties = {
		placeholder,
		type : "text",
		value,
		onFocus,
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
	const isExtended = props.options.length > 0;
	const [isFocused, setFocused] = useState(false);
	
	return (
		<div className="input-simple-container">
			<SimpleInput setFocused={setFocused} isExtended={isExtended && isFocused} {...props}></SimpleInput> 
			<InputSuggestions show={isExtended && isFocused} setFocused={setFocused} {...props}></InputSuggestions>
			<InputErrors {...props}></InputErrors>
		</div>	
	);
};

InputContainer.propTypes = {
	options : PropTypes.oneOf([PropTypes.arrayOf(PropTypes.object), []]),
	value : PropTypes.string.isRequired,
	onChange : PropTypes.func.isRequired,
	placeholder: PropTypes.string,
	required: PropTypes.bool,
	isExtended: PropTypes.bool
}

InputContainer.defaultProps = {
	options : [],
	placeholder : "",
	required : false,
	isExtended : false
}

export default InputContainer;
