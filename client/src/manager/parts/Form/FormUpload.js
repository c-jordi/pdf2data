import axios from "axios"

class FormUpload {
    constructor(params, state, callback){
        this.params = params
        this.state = state
        this.callback = callback
    }

    async run(){

        const postObj = {
            name : this.params.name,
            data : this.state
        }

        const res = await axios.post(this.params.endpoint, postObj, {
            headers:{    
                'Content-Type': 'multipart/form-data'
            },
        });

        if (res.status === 200){
            this.callback()
        }
    }

}

export default FormUpload;