"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
class ExtensionLoadError extends Error {
    constructor(
    /**
     * failed extension
     */
    extension, 
    /**
     * extension error
     */
    originalError, 
    /**
     * extension formatted / handled error message
     */
    msg) {
        super();
        this.extension = extension;
        this.originalError = originalError;
        this.msg = msg;
    }
    toString() {
        return `failed to load extension: ${this.extension.name} with error:

${this.msg || this.originalError.stack}`;
    }
}
exports.default = ExtensionLoadError;
