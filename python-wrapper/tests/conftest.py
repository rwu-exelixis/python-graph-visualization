import os
from typing import Any, Generator

import pytest


def pytest_addoption(parser: Any) -> None:
    parser.addoption(
        "--include-neo4j-and-gds",
        action="store_true",
        help="include tests requiring a Neo4j instance with GDS running",
    )


def pytest_collection_modifyitems(config: Any, items: Any) -> None:
    if not config.getoption("--include-neo4j-and-gds"):
        skip = pytest.mark.skip(reason="skipping since requiring Neo4j instance with GDS running")
        for item in items:
            if "requires_neo4j_and_gds" in item.keywords:
                item.add_marker(skip)


@pytest.fixture(scope="package")
def gds() -> Generator[Any, None, None]:
    from gds_helper import aura_api, connect_to_plugin_gds, create_aurads_instance
    from graphdatascience import GraphDataScience

    NEO4J_URI = os.environ.get("NEO4J_URI")

    if NEO4J_URI:
        gds = connect_to_plugin_gds(NEO4J_URI)
        yield gds
        gds.close()
    else:
        api = aura_api()
        id, dbms_connection_info = create_aurads_instance(api)
        yield GraphDataScience(
            endpoint=dbms_connection_info.uri,
            auth=(dbms_connection_info.username, dbms_connection_info.password),
            aura_ds=True,
            database="neo4j",
        )

        api.delete_instance(id)
