import BaseListInput from "../BaseListInput";
import {getRandomColor, isColorValid} from "../../../../shared/services/utils"

import "./style.scss";

export default class LabelListInput extends BaseListInput{

    createItem(){
        const color = getRandomColor();
        return {text:"", color, colortext: color}
    }

    handleTextChange(callback){
        return (evt) => {
            callback({type:"update",value: {text:evt.target.value}})
        }
    }

    handleColorChange(callback){
        return (evt) => {
            const newColor = evt.target.value.toUpperCase()

            if (newColor.length < 2){
                callback({type:"update",value: {colortext:"#"}})
            }
            else if(isColorValid(newColor)){
                callback({type:"update",value: {color:newColor, colortext:newColor}})
            }
            else {
                callback({type:"update",value: {colortext:newColor}})
            }
        }
    }


    renderItem(item, onChange){
        return <div className="labelinput">
                <input type="text" className="text" placeholder={"Enter label name"} onChange={this.handleTextChange(onChange)} value={item.text}/>
                <div className="color">
                    <input type="text" value={item.colortext} onChange={this.handleColorChange(onChange)} maxLength={7} autoComplete={"off"}  spellCheck="false"></input>
                    <div className="ind" style={{backgroundColor:item.color}}></div>
                </div>
            </div>
    }   
    
}

