import {SimpleButton} from "../../../components/inputs";
import { BiExport, BiArrowBack } from "react-icons/bi";
import {useState} from "react"
import {Redirect} from 'react-router-dom'


const Header = (props) => {
    console.log("headstate", props)

    const [state, setState] = useState({_return: false})

    if (state._return){
        return <Redirect to="/projects"></Redirect>
    }

    const hideLongText = (text, maxLength) => {
        if (text.length > maxLength){
            return text.slice(0, maxLength) + "..."
        }
        return text
    }

    const info = props.state

    return  <div className="project-header">
        <div className="left"><BiArrowBack onClick={()=>setState({...state,_return:true})}/></div>
        <div className="center">
            <div className="top"><div className='name'>{info.name}</div></div>
            <div className="bottom">
                <div className="description">{hideLongText(info.description, 40)}</div>
                <div className="author">{info.author}</div>
            </div>
            
        </div>
        <div className="right">
            <SimpleButton> <BiExport/> Export</SimpleButton>
        </div>
        
    </div>
}

export default Header;