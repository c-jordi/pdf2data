import { BiArrowBack } from "react-icons/bi";
import "./style.scss";

const Toolbar = () => {
    return 	<div className="toolbar">
			<div className="close"><BiArrowBack/> <span>Return</span></div>
            <div className="title">Case study 1</div>
            <div className=""></div>
       
		</div>
}

export default Toolbar;