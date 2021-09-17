import { BiArrowBack } from "react-icons/bi";
import "./style.scss";

const Header = (props) => {
    const handleClick = () => {
        props.notify({type: 'redirect', _sync: false})
    }

    return <div className="d-header" style={{'bottom':props.bottom}}>
			<div className="close" onClick={handleClick}><BiArrowBack/> <span>Return</span></div>
            <div className="title">Case study 1</div>
            <div className="short"></div>   
		</div>

}

export default Header;