import React, {useEffect, useState} from "react";
import Header from "./Header"
import Overview from "./Overview"
import Settings from "./Settings"
import {Redirect} from 'react-router-dom'
import {Container} from "../../../components/views";
import { NavPanel} from "../../../components/navs"
import Sidebar from "../../../parts/Sidebar"
import "./style.scss";


const EditProject = (props) => {

    const {uid} = props.match.params;
    const [state, setState] = useState({_loading:true});


    const fetchProject = async () => {
        const resp = await fetch(`http://localhost:8888/projects/${uid}`, {
            method: "get",
            headers: {
                'Origin': 'http://localhost:2000',
                'Access-Control-Request-Headers': 'Origin, Accept, Content-Type',
                'Access-Control-Request-Method': 'GET'
            }
        })
        const result = await resp.json()
        setState({...state, result, _loading:false})
    }

    useEffect(()=>{
        if (state._loading) fetchProject()
    },)

    if (state._loading){
        return <>
			<Sidebar active={"/project/edit"}></Sidebar>
			<Container>
                Loading..
			</Container>
		</>
    }

    if (state._invalid){
        return <Redirect to={"/projects"}></Redirect>
    }

    const panels = [
        {label: "Overview", content : <Overview state={state.result}/>},
        {label: "Settings", content: <Settings state={state.result}/>}
    ]
    

	return (
		<>
			<Sidebar active={"/project/edit"}></Sidebar>
			<Container>
                <Header state={state.result}></Header>
                <NavPanel panels={panels}></NavPanel>
			</Container>
		</>
	);
};

export default EditProject;
