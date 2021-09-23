import {saveObject, getSavedObject} from "../../../shared/services/autosave";

class ViewController {
    constructor(){
        this.canvas = null;
        this.context = null;
        this.overlay = null;
        this.background = null;
        this.assets = null;
        this.image = null;
        this.annotations = null;
        this.queue = [];
        this.frameId = null;
        this._cachetime = 0;

        this.view = {
            dx : 0,
            dy : 0,
            sx : 0,
            sy : 0,
            sWidth : 0,
            sHeight : 0,
            dWidth : 0,
            dHeight: 0,
            scale : 1,
        }

        this.settings = {
            wPadding: 20,
            hPadding: 30,
            zoomSensitivity : .002
        }

        this.draw = this.draw.bind(this)
        this.zoom = this.zoom.bind(this)
        this.load = this.load.bind(this)
        this.help = this.help.bind(this)
        this.clear = this.clear.bind(this)
        this.cache = this.cache.bind(this)
        this.attach = this.attach.bind(this)
        this.append = this.append.bind(this)
        this.connect = this.connect.bind(this)
        this.project = this.project.bind(this)
        this.display = this.display.bind(this)
        this.onWheel = this.onWheel.bind(this)
        this.annotate = this.annotate.bind(this)
        this.runQueue = this.runQueue.bind(this)
        this.endQueue = this.endQueue.bind(this)
        this.autoscale = this.autoscale.bind(this)
        this.onMouseUp = this.onMouseUp.bind(this)
        this.onMouseDown = this.onMouseDown.bind(this)
        this.onMouseMove = this.onMouseMove.bind(this)
        this.addAnnotation = this.addAnnotation.bind(this)
        this.editAnnotation = this.editAnnotation.bind(this)
        this.showAnnotation = this.showAnnotation.bind(this)
    }

    attach(canvas, overlay){
        this.canvas = canvas;
        this.context = canvas.getContext("2d")
        this.overlay = overlay;
        this.background = overlay.querySelector(".background")
        this.recenterBtn = overlay.querySelector(".controls .recenter")
        this.addEventListeners()
    }

    connect(notify){
        this.notify = notify;
    }

    append(assets){
        this.assets = assets;
        const image = assets.find(({type})=>type==="image")
        this.image = image? image.data.image : null
        this.annotations = assets.find(({type})=>type==="annotations")
    }

    display(){
        if (this.image){
            this.load()
            this.runQueue()
        }
    }

    cache(){
        if ((new Date().getTime() - this._cachetime) > 200){
            saveObject("interactive-view-", {...this.view})
            this._cachetime = new Date().getTime();
        }
    }

    load(){
        const view = getSavedObject("interactive-view-");
        if (view.sWidth === this.image.width && view.sHeight === this.image.height){
            this.view = view;
        } else {
            this.autoscale()
        }
    }


    runQueue(){
        this.queue.forEach(action=>action());
        this.queue = []
        this.clear()
        this.draw()
        this.annotate()
        this.help()
        this.cache()
        this.frameId = window.requestAnimationFrame(this.runQueue)
    }

    endQueue(){
        window.cancelAnimationFrame(this.frameId)
    }

    pan(mx,my){
        this.view.dx = this.view.dx + mx;
        this.view.dy = this.view.dy + my;
    }

    zoom(lx,ly,delta){
        if ((this.view.scale + delta) < 0.2 || (this.view.scale + delta) > 50) return;
        this.view.dx = Math.round(this.view.dx - delta * (lx - this.view.dx) / this.view.scale)
        this.view.dy = Math.round(this.view.dy - delta * (ly - this.view.dy) / this.view.scale)
        this.view.scale = this.view.scale + delta;
        this.view.dWidth = Math.round(this.image.width * this.view.scale)
        this.view.dHeight = Math.round(this.image.height * this.view.scale)
    }

    autoscale(){
        const wRatio = this.image.width / (this.canvas.width - 2*this.settings.wPadding)
        const hRatio = this.image.height / (this.canvas.width - 2*this.settings.hPadding)
        if (hRatio > wRatio){
            this.view.scale = 1/hRatio; 
            this.view.dy = this.settings.hPadding;
            this.view.dx = Math.floor((this.canvas.width - this.image.width * this.view.scale)/2)     
        } else {
            this.view.scale = 1/wRatio;
            this.view.dy = Math.floor((this.canvas.height - this.image.height * this.view.scale)/2)
            this.view.dx = this.settings.wPadding;
        }
        this.view.dWidth = Math.round(this.image.width * this.view.scale)
        this.view.dHeight = Math.round(this.image.height * this.view.scale)
        this.view.sx = 0;
        this.view.sy = 0;
        this.view.sWidth = this.image.width;
        this.view.sHeight = this.image.height;

        this.view._auto_scale = this.view.scale;
        this.view._auto_dx = this.view.dx;
        this.view._auto_dy = this.view.dy;
    }

    clear(){
        this.context.clearRect(0,0,this.canvas.width,this.canvas.height)

    }

    draw(){
        const {sx, sy, sWidth, sHeight, dx, dy, dWidth, dHeight} = this.view;
        this.context.drawImage(this.image,sx, sy, sWidth, sHeight, dx, dy, dWidth, dHeight)
    }

    project(bbox){
        const [aw,ah] = [bbox[2]-bbox[0], bbox[3]-bbox[1]];
        return [
            Math.round(this.view.dx + bbox[0] * this.view.scale),
            Math.round(this.view.dy + bbox[1] * this.view.scale), 
            Math.round(aw * this.view.scale),
            Math.round(ah * this.view.scale)
        ]
    }

    showAnnotation(annotation){
        if (!annotation.dom){
            annotation = this.addAnnotation(annotation)
        }
        annotation = this.editAnnotation(annotation)
        return annotation
    }

    addAnnotation(annotation){
        const that = this;
        console.log(that)
        const box = document.createElement("div");
        box.className = 'box'
        box.innerHTML = "<div class='label'></div>"
        this.overlay.prepend(box)
        box.addEventListener("click", () => that.notify({_sync:false,type:"test"}))
        annotation.dom = box
        return annotation
    }



    editAnnotation(annotation){
        const {bbox, color, label, dom} = annotation;
        const [dx,dy,w,h] = this.project(bbox)
        const border = 1 + this.view.scale; 
        const fontSize = Math.round(this.image.height*this.view.scale * .02);
        const style =  `left:${dx}px;top:${dy}px;width:${w}px;height:${h}px;border:${border}px solid ${color};border-radius: 4px;color: ${color};font-size:${fontSize}px;`
        dom.setAttribute("style",style);
        dom.querySelector(".label").innerText = label;
        return annotation;
    }


    annotate(){
        if (this.annotations){
            this.annotations.data = this.annotations.data.map(annotation=>this.showAnnotation(annotation))
        }
    }

    help(){
        // Recenter
        if (this.view._auto_scale === this.view.scale && 
        this.view._auto_dx === this.view.dx &&
        this.view._auto_dy === this.view.dy){
            this.overlay.setAttribute("data-recenter-active",false);
        }else {
            this.overlay.setAttribute("data-recenter-active",true);
        }
    }

    addEventListeners(){
        this.background.addEventListener("mousedown", this.onMouseDown)
        this.background.addEventListener("wheel", this.onWheel)
        this.recenterBtn.addEventListener("click", this.autoscale)
    }

    removeEventListeners(){
        this.background.removeEventListener("mousedown", this.onMouseDown)
        this.background.removeEventListener("wheel", this.onWheel)
        this.recenterBtn.removeEventListener("click", this.autoscale)
    }

    onMouseDown(){
        window.addEventListener("mousemove",this.onMouseMove)
        window.addEventListener("mouseup", this.onMouseUp)
        document.body.style.cursor = "grabbing";
    }

    onMouseMove({movementX, movementY}){
        this.queue.push(()=>this.pan(movementX, movementY))
    }

    onMouseUp(){
        window.removeEventListener("mousemove", this.onMouseMove)
        window.removeEventListener("mouseup", this.onMouseUp)
        document.body.style.cursor = "default"
    }

    onWheel({layerX, layerY, wheelDelta}){
        this.queue.push(()=>this.zoom(layerX, layerY, wheelDelta* this.settings.zoomSensitivity * this.view.scale))
    }

    detach(){
        if (this.canvas) this.removeEventListeners();
        if (this.frameId) this.endQueue();
    }


}

export default ViewController