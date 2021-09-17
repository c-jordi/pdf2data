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

beforeEach(() => {
  // global.sessionStorage = new StorageMock();
});


test("saves object to the browser cache", () =>{
  saveObject("test-", {name : {value:"Peter"}, job:"lawyer"})
  expect(getSavedObject("test-")).toMatchObject({name : {value:"Peter"}, job:"lawyer"})
})

test("clears object from the browser cache", () => {
  saveObject("test-", {name : {value:"Peter"}, job:"lawyer"})
  clearSavedObjects("test-")
  expect(getSavedObject("test-")).toMatchObject({})
})

test("does not store to the cache hidden fields", () => {
  saveObject("hiddentest-", {visible: true, _nothidden:true, __hidden : false})
  expect(getSavedObject("hiddentest-")).toMatchObject({visible: true,_nothidden:true})
})