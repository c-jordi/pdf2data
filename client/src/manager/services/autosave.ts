export function saveObject(prefix: string, obj: object) : void {
	Object.keys(obj).forEach((key : string) => {
		const value = (obj as any)[key];
		saveInputValue(prefix + key, (typeof value === "object")?JSON.stringify(value): value)
	})
}

export function getSavedObject(prefix: string) : object {
	let formObj:object = {};
	for (let i:number=0;i<global.sessionStorage.length; i++) {	
		const key:string = global.sessionStorage.key(i) || "";
		if (key.startsWith(prefix)) {
			const value: string= global.sessionStorage.getItem(key) || "";
			(formObj as any)[key.slice(prefix.length)] = JSON.parse(value);
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

