import BaseList from "../BaseList";
import FileUpload from "./FileUpload"

import "./style.scss";

export default class FileList extends BaseList{

    createItem(){
        return {_status:"empty"}
    }

    handleChange(callback){
        return (evt) => {
            console.log(evt)
            if(evt.target.files.length){
                const file = evt.target.files[0];
                new FileUpload(file,callback).run() 
            }
            callback({type:"update",value: {_status:'uploading'}})
        }
    }


    renderItem(item, onChange){
        switch(item._status){
            case "empty":
                return <div className="fileinput"><div className="empty">Click here to upload</div><input type="file" key={item.value} onChange={this.handleChange(onChange)} multiple={false}></input></div>
            case "uploading":
                return <div className="fileinput"><div className="loading">Loading</div></div>
            case "uploaded":
                return <div className="fileinput"><div className="loaded"><div className="filename">{item.filename}</div> <div className="size">{item.size}</div></div></div>
            default: 
                return
        }

    }   
    
}

