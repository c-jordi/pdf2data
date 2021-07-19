import {Section} from "../views"
import {MultiLineInput, SimpleInput, RadioInput, SubmitButton} from "../inputs"
import {BaseList, FileList} from "../listinputs"

export function renderElement(el, state, formCallback){

    let props;
    // Stateless components
    switch(el.type){
        case "title":
            return <h2 key={el.content}>{el.content}</h2>
        case "section":
            props = {...el, children: el.content.map(child=>renderElement(child,state,formCallback))}
            return <Section {...props}></Section>
        default:
            break;
    }

    // Stateful components
    const value = (el.name && state[el.name] ? state[el.name].value : undefined);
    const onChange = (action) => {formCallback({origin:el,action})}
    
    switch(el.type){
        case "simple":
            props = {...el, value, onChange};
            return <SimpleInput {...props}></SimpleInput>
        case "multi":
            props = {...el, value, onChange};
            return <MultiLineInput {...props}></MultiLineInput>
        case "radio":
            props = {...el, value, onChange}
            return <RadioInput {...props}></RadioInput>
        case "list":
            props = {...el, value, onChange}
            return <BaseList {...props}></BaseList>
        case "filelist":
            props = {...el, value, onChange}
            return <FileList {...props}></FileList>
        case "submit":
            props = {...el, onClick: onChange}
            return <SubmitButton {...props}></SubmitButton>
        default:
            return;
    }
}