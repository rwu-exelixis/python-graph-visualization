import { NVL } from '@neo4j-nvl/base'
import type { Node, NvlOptions, Relationship } from '@neo4j-nvl/base'
import { DragNodeInteraction, PanInteraction, ZoomInteraction } from '@neo4j-nvl/interaction-handlers'

class PyNVL {
  nvl: NVL

  zoomInteraction: ZoomInteraction

  panInteraction: PanInteraction

  dragNodeInteraction: DragNodeInteraction

  constructor(
    frame: HTMLElement,
    nvlNodes: Node[] = [],
    nvlRels: Relationship[] = [],
    options: NvlOptions = {},
    callbacks = {}
  ) {
    this.nvl = new NVL(frame, nvlNodes, nvlRels, options, callbacks)
    this.zoomInteraction = new ZoomInteraction(this.nvl)
    this.panInteraction = new PanInteraction(this.nvl)
    this.dragNodeInteraction = new DragNodeInteraction(this.nvl)
  }
}

export { PyNVL as NVL }
