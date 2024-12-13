from neo4j_viz import RenderOptions


def test_render_options() -> None:
    options = RenderOptions(layout=RenderOptions.Layout.FORCE_DIRECTED)

    assert options.to_dict() == {"layout": "forcedirected", "maxZoom": 10, "minZoom": 0.075}
