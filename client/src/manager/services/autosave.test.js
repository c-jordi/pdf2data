import {saveObject, getSavedObject, clearSavedObjects} from "./autosave.ts";

class StorageMock {
    constructor() {
      this.store = {};
    }
  
    clear() {
      this.store = {};
    }

    key(item){
      return Object.keys(this.store)[item];
    }

  
    getItem(key) {
      return this.store[key] || null;
    }
  
    setItem(key, value) {
      this.store[key] = String(value);
    }
  
    removeItem(key) {
      delete this.store[key];
    }
  };


test("autosaves object to the browser cache", () =>{

  saveObject("try-", {name : {value:"Peter"}, job:"lawyer"})

  let saved = getSavedObject("try-name");
  expect(saved).toMatchObject({"":{value:'Peter'}})
})
