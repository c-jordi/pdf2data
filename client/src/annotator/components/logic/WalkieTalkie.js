import React, {Component} from 'react'
import FancyWebSocket from "../../../../services/fancywebsocket";


class WalkieTalkie extends Component {
    constructor(props){
        super(props)
        this.uid = props.uid

        this.state = {
            _connecting : true
        }

        this.ws = new FancyWebSocket('ws://localhost:8888/annotate')
        this.updateState = this.updateState.bind(this)
        this.onOpen = this.onOpen.bind(this)
    }

    updateState(update){
        this.setState({...this.state,...update})
    }

    onOpen(){
        this.updateState({_connecting:false})
    }

    componentDidMount() {
        this.ws.bind("open", this.onOpen)
    }

    componentWillUnmount(){
        this.ws.close()
    }

    render(){

        if (this.state._connecting){
            return <div>Connecting...</div>
        }

        const {ws, uid} = this
        return <>
            {React.Children.map(this.props.children, (child) => {
            return React.cloneElement(child, {ws,uid});
            })}
        </>
    }
}   

export default WalkieTalkie;