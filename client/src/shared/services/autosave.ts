export function saveObject(prefix: string, obj: object) : void {
	Object.keys(obj).forEach((key : string) => {
		if (!(key.startsWith("__"))){
			const value = (obj as any)[key];
			saveInputValue(prefix + key, (typeof value === "object")?JSON.stringify(value): value)
		}
	})
}

export function getSavedObject(prefix: string) : object {
	let formObj:object = {};
	for (let i:number=0;i<global.sessionStorage.length; i++) {	
		const key:string = global.sessionStorage.key(i) || "";
		if (key.startsWith(prefix)) {
			const value: string= global.sessionStorage.getItem(key) || "";
			(formObj as any)[key.slice(prefix.length)] = isJson(value)?JSON.parse(value):value;
		}
	}
	return formObj;
}

export function saveInputValue(name:string, value:string): void{
	global.sessionStorage.setItem(name,value)
}


export function getSavedInputValue(name:string): string {
	return global.sessionStorage.getItem(name) || ""
}

export function clearSavedObjects(prefix:string = ""): void{
	if (prefix !== ""){
		const storageCount = global.sessionStorage.length;
		const keysToRemove : any = [];
		for (let i:number=0;i<storageCount; i++) {	
			const key:string = global.sessionStorage.key(i) || "";
			if (key.startsWith(prefix)) keysToRemove.push(key)
		}
		keysToRemove.forEach((key:string) => global.sessionStorage.removeItem(key))
	}
	else {
		global.sessionStorage.clear()
	}
}

function isJson(str:string):boolean {
    try {
        JSON.parse(str);
    } catch (e) {
        return false;
    }
    return true;
}