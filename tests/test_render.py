from IPython.display import HTML

from neo4j_viz.nvl import NVL


def test_basic_render() -> None:
    nvl = NVL()

    nodes = [
        {"id": "4:d09f48a4-5fca-421d-921d-a30a896c604d:0", "caption": "Person"},
        {"id": "4:d09f48a4-5fca-421d-921d-a30a896c604d:6", "caption": "Product"},
        {"id": "4:d09f48a4-5fca-421d-921d-a30a896c604d:11", "caption": "Product"},
        {"id": "4:d09f48a4-5fca-421d-921d-a30a896c604d:12", "caption": "Product"},
        {"id": "4:d09f48a4-5fca-421d-921d-a30a896c604d:1", "caption": "Person"},
        {"id": "4:d09f48a4-5fca-421d-921d-a30a896c604d:7", "caption": "Product"},
        {"id": "4:d09f48a4-5fca-421d-921d-a30a896c604d:8", "caption": "Product"},
    ]
    relationships = [
        {
            "id": "5:d09f48a4-5fca-421d-921d-a30a896c604d:1152921504606846976",
            "from": "4:d09f48a4-5fca-421d-921d-a30a896c604d:0",
            "to": "4:d09f48a4-5fca-421d-921d-a30a896c604d:6",
            "caption": "BUYS",
        },
        {
            "id": "5:d09f48a4-5fca-421d-921d-a30a896c604d:1155173304420532224",
            "from": "4:d09f48a4-5fca-421d-921d-a30a896c604d:0",
            "to": "4:d09f48a4-5fca-421d-921d-a30a896c604d:11",
            "caption": "BUYS",
        },
        {
            "id": "5:d09f48a4-5fca-421d-921d-a30a896c604d:1157425104234217472",
            "from": "4:d09f48a4-5fca-421d-921d-a30a896c604d:0",
            "to": "4:d09f48a4-5fca-421d-921d-a30a896c604d:12",
            "caption": "BUYS",
        },
        {
            "id": "5:d09f48a4-5fca-421d-921d-a30a896c604d:1157425104234217473",
            "from": "4:d09f48a4-5fca-421d-921d-a30a896c604d:1",
            "to": "4:d09f48a4-5fca-421d-921d-a30a896c604d:7",
            "caption": "BUYS",
        },
        {
            "id": "5:d09f48a4-5fca-421d-921d-a30a896c604d:1152921504606846977",
            "from": "4:d09f48a4-5fca-421d-921d-a30a896c604d:1",
            "to": "4:d09f48a4-5fca-421d-921d-a30a896c604d:8",
            "caption": "BUYS",
        },
    ]

    html = nvl.render(nodes, relationships)

    assert isinstance(html, HTML)
