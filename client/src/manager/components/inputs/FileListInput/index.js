import BaseListInput from "../BaseListInput";
import FileUpload from "./FileUpload"

import "./style.scss";

const TIMEOUT = 10000;

export default class FileListInput extends BaseListInput{

    constructor(props){
        super(props)

        this.handleChange = this.handleChange.bind(this)
    }

    createItem(){
        return {_status:"empty"}
    }

    handleChange(callback){
        return (evt) => {
            if(evt.target.files.length){
                const file = evt.target.files[0];
                new FileUpload(file,callback).run() 
            }
        }
    }




    renderItem(item, onChange){
        switch(item._status){
            case "empty":
                return <div className="fileinput"><div className="empty">Click here to upload</div><input type="file" key={item.value} onChange={this.handleChange(onChange)} multiple={false}></input></div>
            case "uploading":
                return <div className="fileinput"><div className="loading">Loading...</div></div>
            case "uploaded":
                return <div className="fileinput"><div className="loaded"><div className="filename">{item.filename}</div> <div className="size">{item.size}</div></div></div>
            case "error":
                return <div className="fileinput"><div className="error">Sorry! The upload has failed, please try again.</div></div>
            default: 
                return
        }

    }   
    
}

