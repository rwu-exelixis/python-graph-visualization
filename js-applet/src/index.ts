import { FreeLayoutType, NVL } from '@neo4j-nvl/base'
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
    this.nvl = new NVL(frame, nvlNodes, nvlRels, { ...options, disableTelemetry: true }, callbacks)
    this.zoomInteraction = new ZoomInteraction(this.nvl)
    this.panInteraction = new PanInteraction(this.nvl)
    this.dragNodeInteraction = new DragNodeInteraction(this.nvl)

    if (options.layout === FreeLayoutType) {
      this.nvl.setNodePositions(nvlNodes, false)
    }
  }
}

export { PyNVL as NVL }
