import { CLI } from '../cli';
export declare class BaseCompiler {
    private cli;
    constructor(cli: CLI);
    config(): {
        cjs: string;
    };
    main(): {
        synopsis: string;
        report: () => string;
    };
    compile(): string;
}
