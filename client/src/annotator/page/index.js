import {Component} from "react"
import {Redirect} from 'react-router-dom'
import {Header, Body, Left, Center, Right} from "../components/views"
import {WalkieTalkie, Dispatcher, reduceState} from "../components/logic"
import Interactive from "../../../parts/Interactive"

import "./style.scss";


class Annotator extends Component {
	constructor(props){
		
		super(props)

		this.uid = props.uid;
		this.ws = props.ws;
		this.state = {
			_redirect : false
		}

		this.dispatcher = new Dispatcher(this.ws)

		this.updateState = this.updateState.bind(this)
		this.check = this.check.bind(this)
		this.invalidate = this.invalidate.bind(this)
		this.callback = this.callback.bind(this)
		this.check()
	}

	updateState(update){
        this.setState({...this.state,...update})
    }

	componentDidMount(){
		this.load()
	}

	invalidate(){
		this.updateState({_redirect : true})
	}

	check(){
		this.ws.bind("invalidated",this.invalidate).send("validate",this.uid)
	}

	load(){
		this.dispatcher.bind(this.callback)
	}

	callback(action){
		this.setState(reduceState(this.state, action))
	}

	
	render(){

		if (this.state._redirect){
			return <Redirect to="/projects"></Redirect>
		}

		const {notify} = this.dispatcher;

		return <div className="annotator">
			<Header notify={notify}></Header>	
			<Body>
				<Left></Left>
				<Center>
					<Interactive data={
						{image: "http://0.0.0.0:8888/storage/test_image.png",
						annotations: [
							{bbox: [100,100,200,200], properties:{text:"No text", label:"Headline", color: "#9r4"}},
							{bbox: [300,300,400,400], properties:{text:"Some more text", label:"Caption", color: "#f40"}}
						]}
					}></Interactive>
				</Center>
				<Right></Right>
			</Body>
		</div>
	}
}

const AnnotatorContainer = (props) => {
	return <WalkieTalkie uid={props.match.params.uid}>
		<Annotator></Annotator>
	</WalkieTalkie>
}

export default AnnotatorContainer;