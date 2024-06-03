"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const harmony_error_1 = require("./harmony-error");
class ExtensionPotentialCircular extends harmony_error_1.HarmonyError {
    constructor(
    /**
     * failed extension
     */
    extension, 
    /**
     * valid extensions dependencies
     */
    validDeps) {
        super();
        this.extension = extension;
        this.validDeps = validDeps;
    }
    toString() {
        return `Failed to load the dependencies for extension . 
This may result from a wrong import or from circular dependencies in imports. 
The following dependencies succeeded loading:`;
    }
}
exports.default = ExtensionPotentialCircular;
