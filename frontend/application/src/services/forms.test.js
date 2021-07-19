import {getCachedInputValue, setCachedInputValue, clearCachedInputValues} from "./forms.ts";

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
  
global.sessionStorage = new StorageMock();

test('Form caching services: set, get, clear', () => {
    setCachedInputValue("test-you","1");
    setCachedInputValue("test-you","2");
    setCachedInputValue("test-it","3");
    setCachedInputValue("other-test","a")
    expect(getCachedInputValue("test-you")).toBe("2");
    clearCachedInputValues("test");
    expect(getCachedInputValue("test-you")).toBe("");
    expect(getCachedInputValue("test-it")).toBe("");
    clearCachedInputValues();
    expect(getCachedInputValue("other-test")).toBe("")
});
  