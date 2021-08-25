const reduceState = (state, action) => {

    switch(action.type){
        case "redirect":
            return {...state, _redirect: true}
        default:
            return {}
    }
}

export default reduceState