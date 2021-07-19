export function validateInputValueWithEndpoint(endpoint:string, value:string) {
	return true;
}

export function setCachedInputValue(name:string, value:string): void{
	global.sessionStorage.setItem(name,value)
}

export function getCachedInputValue(name:string): string {
	return global.sessionStorage.getItem(name) || ""
}

export function clearCachedInputValues(prefix:string = ""): void{
	if (prefix !== ""){
		for (let i:number=0;i<global.sessionStorage.length; i++) {	
			const key:string = global.sessionStorage.key(i) || "";
			if (key.startsWith(prefix)) global.sessionStorage.setItem(key,"")
		}
	}
	else {
		global.sessionStorage.clear()
	}
}

