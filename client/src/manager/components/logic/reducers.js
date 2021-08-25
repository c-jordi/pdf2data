// Initialize the state of the form
export function reduceState(state, el){
    let {_names} = state;

    // Check uniqueness
    if (!_names) _names = [];
    if ( _names.includes(el.name)){
        throw new Error(`The name ${el.name} is already present in the form.`)
    }

    // Meta information
    const meta = {
        _validation : {
            tests : el.validation? el.validation : "",
            is_valid : false,
            errors : []
        },
        _type : el.type
    }

    switch (el.type){
        case "simple":
        case "multi":
            return {...state, [el.name] : {value : "", ...meta}, _names:[..._names, el.name]}
        case "list":
            return {...state, [el.name] : {value : [""], ...meta}, _names:[..._names, el.name]}
        case "filelist":
            return {...state, [el.name] : {value : [{_status:"empty"}], ...meta}, _names:[..._names, el.name]}
        case "labellist":
            return {...state, [el.name] : {value : [{_status:"empty", text:"", color:"#3e7be2", colortext: "#3e7be2"}], ...meta}, _names:[..._names, el.name]}
        case "radio":
            return {...state, [el.name] : {options: el.options, value:el.options[0].value, ...meta}, _names:[..._names, el.name]}
        case "checkbox":
            return {...state, [el.name] : {options: el.options, value:{}, ...meta}, _names:[..._names, el.name]}
        case "section":
            return el.content.reduce(reduceState, state)
        default:
            return {...state}
    }
}

// Update the state of the form through callbacks
export function reduceCallback(state, {origin:{name}, action}){
    switch (action.type){
        case "overwrite":
            return {...state, [name]:{...state[name], value:action.value}}
        case "add":
            return {...state, [name]:{...state[name], value:[...state[name].value, action.value]}}
        case "remove":
            return {...state, [name]:{...state[name], value:state[name].value.filter((el,i)=>i!==action.value)}}
        case "replace":
            return {...state, [name]:{...state[name], value:state[name].value.map((el,i)=>(i===action.key)?action.value:el)}}
        case "update":
            return {...state, [name]:{...state[name], value:state[name].value.map((el,i)=>(i===action.key)?{...el,...action.value}:el)}}
        case "log":
            return {...state}
        default:
            return {...state}
    }
}
