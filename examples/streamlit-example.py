import streamlit as st
from IPython.display import HTML
import streamlit.components.v1 as components
from pandas import read_parquet
import pathlib

from neo4j_viz.pandas import from_dfs
from neo4j_viz import VisualizationGraph

# Path to this file
script_path = pathlib.Path(__file__).resolve()
script_dir_path = pathlib.Path(__file__).parent.resolve()


@st.cache_data
def create_visualization_graph() -> VisualizationGraph:
    cora_nodes_path = f"{script_dir_path}/datasets/cora/cora_nodes.parquet.gzip"
    cora_rels_path = f"{script_dir_path}/datasets/cora/cora_rels.parquet.gzip"

    nodes_df = read_parquet(cora_nodes_path)
    nodes_df = nodes_df.rename(columns={"nodeId": "id"})

    rels_df = read_parquet(cora_rels_path)
    rels_df = rels_df.rename(
        columns={"sourceNodeId": "source", "targetNodeId": "target"}
    )

    # Drop the features column since it's not needed for visualization
    # Also numpy arrays are not supported by the visualization library
    nodes_df.drop(columns="features", inplace=True)

    VG = from_dfs(nodes_df, rels_df)
    VG.color_nodes(property="subject")

    return VG


@st.cache_data
def render_graph(
    _VG: VisualizationGraph, height: int, initial_zoom: float = 0.1
) -> HTML:
    return VG.render(initial_zoom=initial_zoom, height=f"{height}px")


VG = create_visualization_graph()

st.title("Neo4j Viz Streamlit Example")
st.text(
    "This is an example of how to use Streamlit with the Graph "
    "Visualization for Python library by Neo4j."
)

with st.sidebar:
    height = st.slider("Height in pixels", 100, 2000, 600, 50)
    show_code = st.checkbox("Show code")

st.header("Visualization")
st.text(
    "A visualization of the famous Cora citation network. Each of its "
    "seven scientific subjects is represented by a different color."
)

components.html(
    render_graph(VG, height=height).data,
    height=height,
)

if show_code:
    st.header("Code")
    st.code(script_path.read_text())
