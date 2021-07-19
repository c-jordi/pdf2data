import React from "react";
import {Container, Section} from "../../../components/views";
import Sidebar from "../../../parts/Sidebar"
import FormHandler from "../../../parts/Form";
import "./style.scss";

import {BiAlignJustify, BiMenu, BiText } from "react-icons/bi";

const formProperties = {
	caching : true
}

const formContent = [
	{type:"title", content: "Project information"},
	{type:"section", header: "Name",caption:"Helpful to quickly find your project", content:[
		{type:"simple", name: "project_name", placeholder:"Enter a name", required:true},
	]},
	{type:"section", header: "Description", caption: "Describe your project in a couple words", content:[
		{type:"multi", name: "project_desc", placeholder:"Enter a description"}
	]},
	{type:"section", header: "Author", caption: "If multiple, seperate names with comma", content:[
		{type:"simple", name: "project_auth", placeholder:"Enter author name(s)"}
	]},
	{type:"title", content:"Experiment definition"},
	{type:"section", header: "Document level", caption: "Once the project has been created, you will not be able to change the document level.", content:[
		{type: "radio", name:"project_lvl", options:[
			{label:<React.Fragment><BiAlignJustify/><span>Page</span></React.Fragment>,value:"page"},
			{label:<React.Fragment><BiMenu/><span>Block</span></React.Fragment>, value:"block"},
			{label:<React.Fragment><BiText/><span>Title</span></React.Fragment>, value:"textline"}
		]}
	]},
	{type:"section", header: "Source folders", caption:"Select the folders containing the data you would like to use in the experiment.", content:[
		{type:"filelist", name:"project_src"}
	]},
	{type:"submit", name: "submit_btn", label:"Create project", action: {type:"send"}}
]


const CreateProject = () => {
	return (
		<>
			<Sidebar active={"/project/create"}></Sidebar>
			<Container>
				<h1>Create a project</h1>
				<FormHandler properties={formProperties} content={formContent}></FormHandler>
			</Container>
		</>
	);
};

export default CreateProject;
