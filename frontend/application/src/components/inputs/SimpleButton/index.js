
import "./style.scss"

const SimpleButton = (props) => {
    return <button className='simple-button' {...props}>
        {props.children}
    </button>
}



export default SimpleButton;