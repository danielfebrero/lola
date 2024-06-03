import { BaseCompiler } from '../base-compiler';
export declare class TypeScript {
    private compiler;
    constructor(compiler: string);
    compile(): string;
    static provider([baseCompiler]: [BaseCompiler]): Promise<TypeScript>;
}
