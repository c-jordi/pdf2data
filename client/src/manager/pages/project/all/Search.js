import React, {useReducer, Component} from "react"
import { BiAlignJustify, BiCog } from "react-icons/bi";
import {SimpleInput} from "../../../components/inputs";
import {NavHorizontal} from "../../../components/navs"
import { Redirect } from 'react-router-dom'

class Search extends Component {
    constructor(props){
        super(props)

        this.state = {
            query : "",
            filter : "",
            suggestions : []
        }

        this.callback = this.callback.bind(this)
        this.navigate = this.navigate.bind(this)
    }

    async getSuggestions(state){
        const resp = await fetch("http://localhost:8888/search", {
			method: "post",
			headers: {
				'Origin': 'http://localhost:2000',
				'Access-Control-Request-Headers': 'Origin, Accept, Content-Type',
				'Access-Control-Request-Method': 'GET'
			},
            body : JSON.stringify({
                query : state.query,
                domain : "all"
            })
		})
		const {suggestions} = await resp.json()
		this.setState({...this.state, ...this.formatSuggestions(suggestions)})
    }

    formatSuggestions(sugs){
        const that = this;
        return {suggestions: sugs.map(sug => {
            return {content: <><BiAlignJustify/><span onClick={()=>{that.navigate(sug.url)}} style={{"flexGrow":1}}>{sug.label}</span><BiCog className="settings" onClick={()=>{that.navigate(sug.settings)}}/></>}
        })}
    }

    navigate(url){
        this.setState({...this.state,_navigate:url})
    }

    update(action, state){
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

    callback(action){
        const updated = this.update(action, this.state)
        this.getSuggestions(updated)
        this.setState(updated)
    }

    render(){
        const {query, suggestions, _navigate} = this.state;
        if (_navigate){
            return <div className="search">
                <Redirect to={_navigate}></Redirect>
            </div>
        }
        return <div className="search">
            <NavHorizontal name="projects-search-filter" menu={[
                    {label:"All", action:() => this.callback({type:"reset_filter"})},
                ]}></NavHorizontal>
            <SimpleInput value={query} options={suggestions} onChange={(el)=>{this.callback({type:"set_query",value:el.value})}} _validation={{is_valid:true}}></SimpleInput>
        </div>;
    }
}


export default Search;


