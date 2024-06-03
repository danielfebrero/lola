/**
 * hook for registering new CLI commands.
 */
export declare const Command: {
    (target: any, propertyKey: string, descriptor: PropertyDescriptor): void;
    hash: string;
};
export declare type CommandDefinition = {
    synopsis: string;
    report: string;
};
export declare class CLI {
    /**
     * registry for the commands hook
     */
    private commands;
    run(): CommandDefinition[];
}
