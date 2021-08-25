import React, {Component} from "react"
import ItemParent from "./ItemParent"
import ItemChild from "./ItemChild"


class ItemList extends Component {

    renderList(data){

        console.log(data)
        return data.map((parent, i) => {
            const _key = "key-parent-" + i;
            if (parent.children){
                const _children = parent.children.map((child,j)=>{
                    const _key = "key-child-" + j;
                    return <ItemChild data={child} key={_key}></ItemChild>
                })
                return <ItemParent data={parent} key={_key}>{_children}</ItemParent>
            }
            return <ItemParent data={parent} key={_key}></ItemParent>
        })
    }

    render(){
        return  <div className="item-list">{this.renderList(this.props.content)}</div>
    }
    
}
  

export default ItemList;