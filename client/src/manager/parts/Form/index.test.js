import {render, fireEvent, screen} from '@testing-library/react'
import FormHandler from "./index";

const formParams = {
	name : "new-project-form",
	autosave : true,
	endpoint : "http://localhost:8888/projects/new",
	redirect : "/projects"
}

const formContent = [
	{type:"title", content: "Project information"},
	{type:"section", header: "Name",caption:"Helpful to quickly find your project", content:[
		{type:"simple", name: "project_name", placeholder:"Enter a name", required:true, validation: "string.string>5.string<50"},
	]},
	{type:"submit", name: "submit_btn", label:"Create project", action: {type:"send"}}
]


test("check if form redirects", () =>{
    const formHandler = new FormHandler({params:formParams, content:formContent})
    
    formHandler._redirect = true;

    // This test is not complete
  })
  