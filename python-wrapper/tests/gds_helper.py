import os

from graphdatascience import GraphDataScience
from graphdatascience.session import DbmsConnectionInfo, SessionMemory
from graphdatascience.session.aura_api import AuraApi
from graphdatascience.session.aura_api_responses import InstanceCreateDetails


def connect_to_plugin_gds(uri: str) -> GraphDataScience:
    NEO4J_AUTH = ("neo4j", "password")
    if os.environ.get("NEO4J_USER"):
        NEO4J_AUTH = (os.environ.get("NEO4J_USER", "DUMMY"), os.environ.get("NEO4J_PASSWORD", "neo4j"))

    return GraphDataScience(endpoint=uri, auth=NEO4J_AUTH, database="neo4j")


def aura_api() -> AuraApi:
    return AuraApi(
        client_id=os.environ["AURA_API_CLIENT_ID"],
        client_secret=os.environ["AURA_API_CLIENT_SECRET"],
        tenant_id=os.environ.get("AURA_API_TENANT_ID"),
    )


def create_aurads_instance(api: AuraApi) -> tuple[str, DbmsConnectionInfo]:
    # Switch to Sessions once they can be created without a DB
    instance_details: InstanceCreateDetails = api.create_instance(
        name="ci-neo4j-viz-session",
        memory=SessionMemory.m_8GB.value,
        cloud_provider="gcp",
        region="europe-west1",
    )

    wait_result = api.wait_for_instance_running(instance_id=instance_details.id)
    if wait_result.error:
        raise Exception(f"Error while waiting for instance to be running: {wait_result.error}")

    wait_result.connection_url

    return instance_details.id, DbmsConnectionInfo(
        uri=wait_result.connection_url,
        username="neo4j",
        password=instance_details.password,
    )
