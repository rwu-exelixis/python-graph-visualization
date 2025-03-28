import os
from typing import Any, Generator

import pytest


def pytest_addoption(parser: Any) -> None:
    parser.addoption(
        "--include-neo4j-and-gds",
        action="store_true",
        help="include tests requiring a Neo4j instance with GDS running",
    )
    parser.addoption(
        "--include-snowflake",
        action="store_true",
        help="include tests requiring a Snowflake connection",
    )


def pytest_collection_modifyitems(config: Any, items: Any) -> None:
    if not config.getoption("--include-neo4j-and-gds"):
        skip = pytest.mark.skip(reason="skipping since requiring Neo4j instance with GDS running")
        for item in items:
            if "requires_neo4j_and_gds" in item.keywords:
                item.add_marker(skip)
    if not config.getoption("--include-snowflake"):
        skip = pytest.mark.skip(reason="skipping since requiring a Snowflake connection")
        for item in items:
            if "requires_snowflake" in item.keywords:
                item.add_marker(skip)


@pytest.fixture(scope="package")
def gds() -> Generator[Any, None, None]:
    from gds_helper import aura_api, connect_to_plugin_gds, create_aurads_instance
    from graphdatascience import GraphDataScience

    use_cloud_setup = os.environ.get("AURA_API_CLIENT_ID", None)

    if use_cloud_setup:
        api = aura_api()
        id, dbms_connection_info = create_aurads_instance(api)

        # setting as environment variables to run notebooks with this connection
        os.environ["NEO4J_URI"] = dbms_connection_info.uri
        os.environ["NEO4J_USER"] = dbms_connection_info.username
        os.environ["NEO4J_PASSWORD"] = dbms_connection_info.password

        yield GraphDataScience(
            endpoint=dbms_connection_info.uri,
            auth=(dbms_connection_info.username, dbms_connection_info.password),
            aura_ds=True,
            database="neo4j",
        )

        # Clear Neo4j_URI after test (rerun should create a new instance)
        os.environ["NEO4J_URI"] = ""

        api.delete_instance(id)
    else:
        NEO4J_URI = os.environ.get("NEO4J_URI", "neo4j://localhost:7687")
        gds = connect_to_plugin_gds(NEO4J_URI)
        yield gds
        gds.close()


@pytest.fixture(scope="package")
def neo4j_session() -> Generator[Any, None, None]:
    import neo4j

    NEO4J_URI = os.environ.get("NEO4J_URI", "neo4j://localhost:7687")

    with neo4j.GraphDatabase.driver(NEO4J_URI) as driver:
        driver.verify_connectivity()
        with driver.session() as session:
            yield session
