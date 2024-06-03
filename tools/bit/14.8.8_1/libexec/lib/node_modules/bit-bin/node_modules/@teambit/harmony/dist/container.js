"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
class Container {
    constructor(instances = new Map()) {
        this.instances = instances;
    }
    register(token, instance) {
        this.instances.set(token, instance);
    }
    resolve(token) {
        return this.instances.get(token);
    }
    static loadWith(defaults) {
        const extensionMap = new Map(defaults.map(extension => [extension.name, extension]));
        return new Container(extensionMap);
    }
}
exports.default = Container;
// A -> B -> C
// A -> C
// instantiate A then B and C
