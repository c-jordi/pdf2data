import React from "react"
import Header from "../Header"
import LeftView from "../LeftView"
import RightView from "../RightView"
import Interactive from "../Interactive"
import "./style.scss"

class Fullscreen extends React.Component {
    constructor(props){
        super(props)

        this.state = {
            innerWidth : window.innerWidth,
            innerHeight : window.innerHeight
        }

        

        this.updateDimensions = this.updateDimensions.bind(this)
    }

    
    componentWillMount(){
        window.addEventListener("resize", this.updateDimensions)
    }

    componentWillUnmount(){
        window.removeEventListener("resize", this.updateDimensions)
    }

    updateDimensions(){
        this.setState({innerWidth:window.innerWidth, innerHeight:window.innerHeight})
    }

    

    render(){
        return <div className='fullscreen'>
            <div className='d-container'>
                <Header notify={this.props.notify} bottom={this.state.innerHeight - 44}></Header>
                <LeftView notify={this.props.notify} right={this.state.innerWidth - 250}></LeftView>
                <Interactive notify={this.props.notify} width={this.state.innerWidth} height={this.state.innerHeight - 44} assets={this.props.assets}></Interactive>
                <RightView notify={this.props.notify} left={this.state.innerWidth - 250}></RightView>
            </div>
        </div>
    }
}

export default Fullscreen;