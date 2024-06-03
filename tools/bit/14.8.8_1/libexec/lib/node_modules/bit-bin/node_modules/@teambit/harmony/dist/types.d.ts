import { Harmony } from './harmony';
/**
 * type definition for the extension provider function.
 */
export declare type ProviderFn = (deps: any, config: any, slots: any, harmony: Harmony) => Promise<any>;
