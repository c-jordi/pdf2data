export function validateState(state){
    const new_state = state._names.map(name => {
        const {_validation: {tests}, value} = state[name];
        const {is_valid, errors} = validateStateInput(tests, value)
        return {...state[name], _validation : {tests, is_valid, errors}}
    })
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
            return [value.length >0, "String cannot be null"]
        case 'string>5':
            return [value.length > 5, "Input is not long enough."]
        case 'string<50':
            return [value.length < 50, "Input must be shorter than 50 characters."]
        default:
            return true;
    }
}

