class Dispatcher {
    constructor(ws){
        this.ws = ws
        this._clientCallback = null;

        this.notify = this.notify.bind(this)
    }

    bind(callback){
        this._clientCallback = callback;
    }

    notify(msg){
        console.log("Notified of:", msg);
        if (msg._sync === false){
            
            return this._clientCallback(msg)
        }

    }

}

export default Dispatcher;