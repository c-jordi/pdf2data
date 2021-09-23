import {useRef, useEffect} from "react"
import {MdFilterCenterFocus} from "react-icons/md";
import {ViewController} from "../../components/logic"
import PropTypes from "prop-types"
import "./style.scss"

const Interactive = (props) => {

    const canvasRef = useRef(null);
    const overlayRef = useRef(null);
    

    const coords = {
        bottom: 0,
        left: 250,
        width: props.width - 500,
        height : props.height,
        top: 44
    }   

    const view = new ViewController()

    useEffect(() => {
        view.attach(canvasRef.current, overlayRef.current)
        view.connect(props.notify)
        view.append(props.assets)
        view.display()

        return () => {view.detach()}
    },[props])


    return <div className='interactive' style={coords} >
        <div className="overlay" ref={overlayRef} width={coords.width} height={coords.height}>
            <div className="controls">
                <div className="recenter"><MdFilterCenterFocus/></div>
            </div>
            <div className="background"></div>
        </div>
        <canvas ref={canvasRef} width={coords.width} height={coords.height}/> 
    </div>
}
 

Interactive.defaultProps = {
    notify : console.log
}

export default Interactive;