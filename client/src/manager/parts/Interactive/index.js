import React, {Component, createRef} from "react"
import "./style.scss"

const AnnotationLayer = () => {
    return <div className="annotations"/>
}

class ResizableContainer extends Component {

    constructor(props){
        super(props)

        this.state = {
            height : 0,
            width : 0
        }

        this.ref = createRef()
        this.fixedRef = createRef()
        this.setupObserver = this.setupObserver.bind(this);
        this.getDimensions = this.getDimensions.bind(this)
    }

    componentDidMount(){
        this.setupObserver()
        this.getDimensions()
    }   

    setupObserver(){
        let options = {
            root : this.ref.current,
            rootMargin : "0px",
            threshold : 1.0
        }
        this.observer = new IntersectionObserver(console.table, options)
        this.observer.observe(this.fixedRef.current)
    }

    getDimensions(){
        const {width, height} = this.ref.current.getBoundingClientRect()
        this.fixedRef.current.width = width;
        this.fixedRef.current.height = height;
        this.setState({width, height})
    }

    render(){
        const {width, height} = this.state;
        return <div className="resizable-container" style={{position:"relative"}} ref={this.ref}>
            <div style={{position:"absolute"}}ref={this.fixedRef}>w</div>
            {React.Children.map(this.props.children, (child) => {
            return React.cloneElement(child, {width, height});
            })}
        </div>
    }
}

class Interactive extends Component {
    constructor(props){
        super(props)

        this.parentRef = createRef()
    }


    render() {
        return <div className='interactive'>
            <ResizableContainer>

            </ResizableContainer>
        </div>
    }
}

export default Interactive;