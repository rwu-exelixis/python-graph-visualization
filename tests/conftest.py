from typing import Any

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
