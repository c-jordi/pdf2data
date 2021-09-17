import PropTypes from "prop-types";
import {BiSearch} from "react-icons/bi";
import {useRef} from "react";
import "./style.scss"

const SearchInput = ({style, value, onChange, placeholder}) => {

    const ref = useRef()

    const handleClick = () => {
        ref.current.focus()
    }

    return <div className='d-search-input' style={style}>
        <BiSearch onClick={handleClick} style={{width:15, marginRight: 6}} className="icon"></BiSearch>
        <input type="text" placeholder={placeholder} value={value} onChange={onChange} ref={ref}></input>
    </div>
}


SearchInput.propTypes = {
	value : PropTypes.string.isRequired,
	onChange : PropTypes.func.isRequired,
	placeholder: PropTypes.string,
    style : PropTypes.object
};

SearchInput.defaultProps = {
	placeholder: "search",
    value : "",
    onChange : (evt) => console.log(evt.target.value),
    style : {},
};


export default SearchInput;