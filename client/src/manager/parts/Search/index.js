import React, {useReducer, Component} from "react"
import {SimpleInput} from "../../components/inputs";
import {NavHorizontal} from "../../components/navs"
import { ItemList } from "../../components/views";
import "./style.scss";


class SearchOutput extends Component {

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

const SearchController = () => {

	const reducer = (action, state) => {
		switch (action.type){
			case "reset_filter" :
				return {...state, filter : ''}
			case "set_filter":
				return {...state, filter: action.value}
			case "set_query":
				return {...state, query: action.value}
			case "set_display":
				return {...state, display: action.value}
			default:
				return {...state}
		}
	}

	const [searchObj, setSearch] = useReducer(reducer, {
		query : "",
		filter : "",
		display : ""
	})

	return <div className="file-search">
		<NavHorizontal name="projects-search-filter" menu={[
                {label:"All", action:() => {setSearch({type:"reset_filter"})}},
            ]}></NavHorizontal>
		<SimpleInput value={searchObj.query} onChange={(el)=>{setSearch({type:"set_query",value:el.value})}}></SimpleInput>
		<NavHorizontal name="projects-search-filter" menu={[
			{label:"List", action:()=>{}},
		]}></NavHorizontal>
		<SearchOutput search={searchObj}></SearchOutput>
	</div>;
};



export default SearchController;
