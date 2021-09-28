import {Component} from "react"
import {ItemList} from "../../../components/views"

class Catalog extends Component {

	state = {
		results : []
	}

	async fetchResults(obj){
		const resp = await fetch("http://localhost:8888/projects", {
			method: "get",
			headers: {
				'Origin': 'http://localhost:2000',
				'Access-Control-Request-Headers': 'Origin, Accept, Content-Type',
				'Access-Control-Request-Method': 'GET'
			}
		})
		const {results} = await resp.json()
		this.setState({...this.state, results})
	}
	
	componentDidMount(){
		this.fetchResults(this.props.search)
	}

	render(){
		return <ItemList content={this.state.results}></ItemList>
	}
}

export default Catalog;