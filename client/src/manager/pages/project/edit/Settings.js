import FormHandler from "../../../parts/Form";

const Settings = ({state}) => {

    const formParams = {
        name : "project-edit-form",
        endpoint : `http://localhost:8888/projects/update`,
        redirect : `/projects`,
        meta : {uid: state.uid}
    }

    const _labels = state.labels.map(label=>({
        text : label.name,
        color: label.color,
        colortext : label.color
    }))


    const formContent = [
        {type:"section", header: "Name",caption:"Helpful to quickly find your project", content:[
            {type:"simple", name: "project_name", value: state.name ,placeholder:"Enter a name", validation: "string.string>5.string<50"},
        ]},
        {type:"section", header: "Description", caption: "Describe your project in a couple words", content:[
            {type:"multi", name: "project_desc", value: state.description, placeholder:"Enter a description"}
        ]},
        {type:"section", header: "Author", caption: "If multiple, seperate names with comma", content:[
            {type:"simple", name: "project_auth", placeholder:"Enter author name(s)", value: state.author, validation: "string.string>3.letters&commas"}
        ]},
        {type:"submit", name: "submit_btn", label:"Save", action: {type:"send"}}
    ]
    

    return <FormHandler params={formParams} content={formContent}></FormHandler>
}

export default Settings