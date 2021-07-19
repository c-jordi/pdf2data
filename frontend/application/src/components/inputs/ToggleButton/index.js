
import "./style.scss"

const ToggleButton = (props) => {
    return <button className='simple-button' {...props}>
        {props.children}
    </button>
}



export default ToggleButton;