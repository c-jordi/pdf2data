import axios from "axios"

class FileUpload {
    constructor(file, onChange){
        this.file = file;
        this.onChange = onChange;
    }

    async run(){
        const formData = new FormData();
        formData.append(
            "fileupload", this.file
        )

        const res = await axios.post('http://localhost:8888/upload', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
        });

        if (res.status === 200){
            this.onChange({type:"update", value:{...res.data, _status : 'uploaded'}})
        }
    }

}

export default FileUpload;