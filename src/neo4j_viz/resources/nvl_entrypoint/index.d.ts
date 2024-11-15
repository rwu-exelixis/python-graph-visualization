import { NVL } from '@neo4j-nvl/base';
import type { Node, NvlOptions, Relationship } from '@neo4j-nvl/base';
import { DragNodeInteraction, PanInteraction, ZoomInteraction } from '@neo4j-nvl/interaction-handlers';
declare class PyNVL {
    nvl: NVL;
    zoomInteraction: ZoomInteraction;
    panInteraction: PanInteraction;
    dragNodeInteraction: DragNodeInteraction;
    constructor(frame: HTMLElement, nvlNodes?: Node[], nvlRels?: Relationship[], options?: NvlOptions, callbacks?: {});
}
export { PyNVL as NVL };
