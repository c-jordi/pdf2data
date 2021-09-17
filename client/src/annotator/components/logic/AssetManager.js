class AssetManager {
    constructor(){

        this.attach = this.attach.bind(this)
        this.add = this.add.bind(this)
        this.clear = this.clear.bind(this)
        this.load = this.load.bind(this)
        this.update = this.update.bind(this)
    }

    attach(get,set){
        this.get = get
        this.set = set
    }

    update(data){
       data.forEach(this.load)
    }

    load(asset){
        switch(asset.type){
            case 'image':
                return this.loadImage(asset)
            default:
                return this.add(asset)
        }
    }

    loadImage(asset){
        const that = this;
        const onLoad = (evt) => {
            asset.data.image = evt.path[0]
            that.add(asset)

            return image.removeEventListener("load", onLoad)
        }
        const image = new window.Image()
        image.src = asset.data.src;
        image.addEventListener("load", onLoad)
    }

    loadAnnotations(asset){
        
    }


    add(asset){
        const assets = this.get()
        if (!assets.find(_asset => _asset.id === asset.id)) this.set([...assets, asset])
    }

    clear(){
        this.set([])
    }

    remove(asset){

    }

}

export default AssetManager;