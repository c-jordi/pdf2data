import {Component} from "react"
import {Redirect} from 'react-router-dom'
import {Header, Body} from "../components/views"
import {WalkieTalkie, Dispatcher, AssetManager, reduceState} from "../components/logic"
import Fullscreen from "../parts/Fullscreen"

import "./style.scss";


class Annotator extends Component {
	constructor(props){
		
		super(props)

		this.uid = props.uid;
		this.ws = props.ws;
		this.state = {
			assets : [],
			_redirect : false,
		}
		this._loaded = false;

		this.dispatcher = new Dispatcher(this.ws)
		this.assetManager = new AssetManager()

		this.updateState = this.updateState.bind(this)
		this.getAssets = this.getAssets.bind(this)
		this.setAssets = this.setAssets.bind(this)
		this.update = this.update.bind(this)
		this.check = this.check.bind(this)
		this.redirect = this.redirect.bind(this)
		this.load = this.load.bind(this)
		this.callback = this.callback.bind(this)
		
	}

	updateState(update){
        this.setState({...this.state,...update})
    }

	getAssets(){
		return this.state.assets
	}

	setAssets(assets){
		this.setState({...this.state, assets})
	}

	componentDidMount(){
		this.check()
		this.connect()
	}


	connect(){
		this.dispatcher.attach(this.callback)
		this.assetManager.attach(this.getAssets, this.setAssets)
	}

	redirect(){
		this.updateState({_redirect : true})
	}

	load(){
		if (!this._loaded) this.ws.bind("update",this.update).send("load",this.uid)
	}

	update(data){
		this.assetManager.update(data)
		this.updateState({data})
	}


	check(){
		this.ws.bind("invalidated",this.redirect).bind("validated",this.load).send("validate",this.uid)
	}


	callback(action){
		this.setState(reduceState(this.state, action))
	}
	
	render(){

		if (this.state._redirect){
			return <Redirect to="/projects"></Redirect>
		}

		const {notify} = this.dispatcher;

		console.log("ASSETS:",this.state.assets)

		return <div className="annotator">
				<Fullscreen notify={notify} assets={this.state.assets}/>
		</div>
	}
}

const AnnotatorContainer = (props) => {
	return <WalkieTalkie uid={props.match.params.uid}>
		<Annotator></Annotator>
	</WalkieTalkie>
}

export default AnnotatorContainer;