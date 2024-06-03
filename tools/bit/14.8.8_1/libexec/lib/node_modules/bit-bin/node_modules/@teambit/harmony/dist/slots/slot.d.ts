import { SlotRegistry } from './registry';
export declare class Slot {
    static withType<T>(): (registerFn: () => string) => SlotRegistry<T>;
}
export declare type SlotProvider<T> = (registerFn: () => string) => SlotRegistry<T>;
