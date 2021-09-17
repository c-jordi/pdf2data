export function validateState(state){
    const {_names} = state;
    let is_state_valid = true;
    _names.forEach(name => {
        const {_validation: {tests}, value} = state[name];
        const {is_valid, errors} = validateStateInput(tests, value)
        is_state_valid = is_state_valid && is_valid;
        state[name] = {...state[name],_validation: {tests,is_valid,errors}}
    })
    state.__valid = is_state_valid;
    return state

}

export function validateStateInput(arg, value){
    const tests = arg.split(".")
    return tests.reduce((acc, test) => {
        const [is_valid,error] = runInputTest(test, value);
        if (is_valid){
            return {is_valid : acc.is_valid && is_valid, errors: acc.errors}
        }
        return {is_valid : false, errors : [...acc.errors, error]}
    }, {is_valid: true, errors : []})
}

function runInputTest(test, value){
    switch (test){
        case 'string':
            return [typeof value === "string", "Not a valid string."]
        case 'number':
            return [typeof value === "number", "Not a valid number."]
        case "string>0":
            return [value.length > 0, "String cannot be null"]
        case "string>3":
            return [value.length > 3, "Input is not long enough."]
        case 'string>5':
            return [value.length > 5, "Input is not long enough."]
        case 'string<50':
            return [value.length < 50, "Input must be shorter than 50 characters."]
        case 'letters&commas':
            return [/^[a-xA-Z\s,]+$/.test(value), "Input can only contain letters and commas."]
        case 'oneuploadmin':
            return [value.reduce((acc,val)=>acc || val._status === 'uploaded', false), "At least one file should be uploaded."]
        case 'validlabelcolor':
            return [value.reduce((acc,val)=>acc && /^#[0-9A-F]{6}$/.test(val.color), true), "Not all label colors are valid."]
        case 'validlabeltext':
            return [value.reduce((acc,val)=>acc && val.text !== '', true), "Please enter text for all labels."]
        case 'uniquelabelcolor':
            return [value.map(el=>el.color).reduce((acc,el,i,arr) => acc && arr.indexOf(el)===i, true), 'All the label colors must be unique.']
        case 'uniquelabeltext':
            return [value.map(el=>el.text).reduce((acc,el,i,arr) => acc && arr.indexOf(el)===i, true), 'Text for each label must be unique.']
        default:
            return [true, ""];
    }
}

