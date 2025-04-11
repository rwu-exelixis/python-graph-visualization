import { FreeLayoutType, NVL } from '@neo4j-nvl/base'
import type { Node, NvlOptions, Relationship } from '@neo4j-nvl/base'
import { DragNodeInteraction, PanInteraction, ZoomInteraction, HoverInteraction } from '@neo4j-nvl/interaction-handlers'

class PyNVL {
  nvl: NVL

  zoomInteraction: ZoomInteraction

  panInteraction: PanInteraction

  dragNodeInteraction: DragNodeInteraction

  constructor(
    frame: HTMLElement,
    tooltip: HTMLElement,
    nvlNodes: Node[] = [],
    nvlRels: Relationship[] = [],
    options: NvlOptions = {},
    callbacks = {}
  ) {

    this.nvl = new NVL(frame, nvlNodes, nvlRels, { ...options, disableTelemetry: true, disableWebWorkers: true, disableAria: true }, callbacks)
    this.zoomInteraction = new ZoomInteraction(this.nvl)
    this.panInteraction = new PanInteraction(this.nvl)
    this.dragNodeInteraction = new DragNodeInteraction(this.nvl)

    const hoverInteraction = new HoverInteraction(this.nvl)

    hoverInteraction.updateCallback('onHover', (element, hitElements, event) => {
      if (element === undefined) {
        tooltip.setHTMLUnsafe("")
        if (tooltip.style.display === "block") {
          tooltip.style.display = "none";
        }
      } else if ("from" in element) {
        const rel = element as Relationship
        if (tooltip.style.display === "none") {
          tooltip.style.display = "block";
        }
        tooltip.setHTMLUnsafe("<b>Source ID:</b> " + rel.from + "</br><b>Target ID:</b> " + rel.to)
      } else if ("id" in element) {
        if (tooltip.style.display === "none") {
          tooltip.style.display = "block";
        }
        tooltip.setHTMLUnsafe("<b>ID:</b> " + element.id)
      }
    })

    if (options.layout === FreeLayoutType) {
      this.nvl.setNodePositions(nvlNodes, false)
    }
  }
}

export { PyNVL as NVL }
