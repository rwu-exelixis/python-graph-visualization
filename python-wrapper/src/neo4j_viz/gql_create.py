import re
import uuid
from typing import Any, Optional

from neo4j_viz import Node, Relationship, VisualizationGraph


def _parse_value(value_str: str) -> Any:
    value_str = value_str.strip()
    if not value_str:
        return None

    # Parse object
    if value_str.startswith("{") and value_str.endswith("}"):
        inner = value_str[1:-1].strip()
        result = {}
        depth = 0
        in_string = None
        start_idx = 0
        for i, ch in enumerate(inner):
            if in_string is None:
                if ch in ["'", '"']:
                    in_string = ch
                elif ch in ["{", "["]:
                    depth += 1
                elif ch in ["}", "]"]:
                    depth -= 1
                elif ch == "," and depth == 0:
                    segment = inner[start_idx:i].strip()
                    if ":" not in segment:
                        return None
                    k, v = segment.split(":", 1)
                    k = k.strip().strip("'\"")
                    result[k] = _parse_value(v)
                    start_idx = i + 1
            else:
                if ch == in_string:
                    in_string = None
        if inner[start_idx:]:
            segment = inner[start_idx:].strip()
            if ":" not in segment:
                return None
            k, v = segment.split(":", 1)
            k = k.strip().strip("'\"")
            result[k] = _parse_value(v)
        return result

    # Parse list
    if value_str.startswith("[") and value_str.endswith("]"):
        inner = value_str[1:-1].strip()
        items = []
        depth = 0
        in_string = None
        start_idx = 0
        for i, ch in enumerate(inner):
            if in_string is None:
                if ch in ["'", '"']:
                    in_string = ch
                elif ch in ["{", "["]:
                    depth += 1
                elif ch in ["}", "]"]:
                    depth -= 1
                elif ch == "," and depth == 0:
                    items.append(_parse_value(inner[start_idx:i]))
                    start_idx = i + 1
            else:
                if ch == in_string:
                    in_string = None
        if inner[start_idx:]:
            items.append(_parse_value(inner[start_idx:]))
        return items

    # Parse boolean, float, int, or string
    if re.match(r"^-?\d+$", value_str):
        return int(value_str)
    if re.match(r"^-?\d+\.\d+$", value_str):
        return float(value_str)
    if value_str.lower() == "true":
        return True
    if value_str.lower() == "false":
        return False
    if value_str.lower() == "null":
        return None
    return value_str.strip("'\"")


def _get_snippet(q: str, idx: int, context: int = 15) -> str:
    start = max(0, idx - context)
    end = min(len(q), idx + context)
    return q[start:end].replace("\n", " ")


def from_gql_create(query: str) -> VisualizationGraph:
    """
    Parse a GQL CREATE query and return a VisualizationGraph object representing the graph it creates.

    All node and relationship properties will be included in the visualization graph.
    If the properties are named as the fields of the `Node` or `Relationship` classes, they will be included as
    top level fields of the respective objects. Otherwise, they will be included in the `properties` dictionary.
    Additionally, a "labels" property will be added for nodes and a "type" property for relationships.

    Please note that this function is not a full GQL parser, it only handles CREATE queries that do not contain
    other clauses like MATCH, WHERE, RETURN, etc, or any Cypher function calls.
    It also does not handle all possible GQL syntax, but it should work for most common cases.

    Parameters
    ----------
    query : str
        The GQL CREATE query to parse
    """

    query = query.strip()
    # Case-insensitive check that 'CREATE' is the first non-whitespace token
    if not re.match(r"(?i)^create\b", query):
        raise ValueError("Query must begin with 'CREATE' (case insensitive).")

    def parse_prop_str(
        prop_str: str, prop_start: int, top_level_keys: set[str]
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        top_level: dict[str, Any] = {}
        props: dict[str, Any] = {}
        depth = 0
        in_string = None
        start_idx = 0
        for i, ch in enumerate(prop_str):
            if in_string is None:
                if ch in ["'", '"']:
                    in_string = ch
                elif ch in ["{", "["]:
                    depth += 1
                elif ch in ["}", "]"]:
                    depth -= 1
                elif ch == "," and depth == 0:
                    pair = prop_str[start_idx:i].strip()
                    if ":" not in pair:
                        snippet = _get_snippet(query, prop_start + start_idx)
                        raise ValueError(f"Property syntax error near: `{snippet}`.")
                    k, v = pair.split(":", 1)
                    k = k.strip().strip("'\"")

                    if k in top_level_keys:
                        top_level[k] = _parse_value(v)
                    else:
                        props[k] = _parse_value(v)

                    start_idx = i + 1
            else:
                if ch == in_string:
                    in_string = None

        if prop_str[start_idx:]:
            pair = prop_str[start_idx:].strip()
            if ":" not in pair:
                snippet = _get_snippet(query, prop_start + start_idx)
                raise ValueError(f"Property syntax error near: `{snippet}`.")
            k, v = pair.split(":", 1)
            k = k.strip().strip("'\"")

            if k in top_level_keys:
                top_level[k] = _parse_value(v)
            else:
                props[k] = _parse_value(v)

        return top_level, props

    def parse_labels_and_props(
        s: str, top_level_keys: set[str]
    ) -> tuple[Optional[str], dict[str, Any], dict[str, Any]]:
        prop_match = re.search(r"\{(.*)\}", s)
        prop_str = ""
        if prop_match:
            prop_str = prop_match.group(1)
            prop_start = query.index(prop_str, query.index(s))
            s = s[: prop_match.start()].strip()
        alias_labels = re.split(r"[:&]", s)
        raw_alias = alias_labels[0].strip()
        final_alias = raw_alias if raw_alias else None

        if prop_str:
            top_level, props = parse_prop_str(prop_str, prop_start, top_level_keys)
        else:
            top_level = {}
            props = {}

        label_list = [lbl.strip() for lbl in alias_labels[1:]]
        if "labels" in props:
            props["__labels"] = props["labels"]
        props["labels"] = sorted(label_list)

        return final_alias, top_level, props

    nodes = []
    relationships = []
    alias_to_id = {}
    anonymous_count = 0

    query = re.sub(r"(?i)^create\s*", "", query, count=1).rstrip(";").strip()
    parts = []
    paren_level = 0
    bracket_level = 0
    current: list[str] = []
    for i, char in enumerate(query):
        if char == "(":
            paren_level += 1
        elif char == ")":
            paren_level -= 1
            if paren_level < 0:
                snippet = _get_snippet(query, i)
                raise ValueError(f"Unbalanced parentheses near: `{snippet}`.")
        if char == "[":
            bracket_level += 1
        elif char == "]":
            bracket_level -= 1
            if bracket_level < 0:
                snippet = _get_snippet(query, i)
                raise ValueError(f"Unbalanced square brackets near: `{snippet}`.")
        if char == "," and paren_level == 0 and bracket_level == 0:
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    parts.append("".join(current).strip())
    if paren_level != 0:
        snippet = _get_snippet(query, len(query) - 1)
        raise ValueError(f"Unbalanced parentheses near: `{snippet}`.")
    if bracket_level != 0:
        snippet = _get_snippet(query, len(query) - 1)
        raise ValueError(f"Unbalanced square brackets near: `{snippet}`.")

    node_pattern = re.compile(r"^\(([^)]+)\)$")
    rel_pattern = re.compile(r"^\(([^)]+)\)-\s*\[\s*:(\w+)\s*(\{[^}]*\})?\s*\]->\(([^)]+)\)$")

    node_top_level_keys = set(Node.model_fields.keys())
    node_top_level_keys.remove("id")

    rel_top_level_keys = set(Relationship.model_fields.keys())
    rel_top_level_keys.remove("id")
    rel_top_level_keys.remove("source")
    rel_top_level_keys.remove("target")

    empty_set: set[str] = set()

    for part in parts:
        node_m = node_pattern.match(part)
        if node_m:
            alias_labels_props = node_m.group(1).strip()
            alias, top_level, props = parse_labels_and_props(alias_labels_props, node_top_level_keys)
            if not alias:
                alias = f"_anon_{anonymous_count}"
                anonymous_count += 1
            if alias not in alias_to_id:
                alias_to_id[alias] = str(uuid.uuid4())
            nodes.append(Node(id=alias_to_id[alias], **top_level, properties=props))
        else:
            rel_m = rel_pattern.match(part)
            if rel_m:
                left_node = rel_m.group(1).strip()
                rel_type = rel_m.group(2).replace(":", "").strip()
                right_node = rel_m.group(4).strip()

                left_alias, _, _ = parse_labels_and_props(left_node, empty_set)
                if not left_alias or left_alias not in alias_to_id:
                    snippet = _get_snippet(query, query.index(left_node))
                    raise ValueError(f"Relationship references unknown node alias: '{left_alias}' near: `{snippet}`.")

                right_alias, _, _ = parse_labels_and_props(right_node, empty_set)
                if not right_alias or right_alias not in alias_to_id:
                    snippet = _get_snippet(query, query.index(right_node))
                    raise ValueError(f"Relationship references unknown node alias: '{right_alias}' near: `{snippet}`.")

                rel_id = str(uuid.uuid4())
                rel_props_str = rel_m.group(3) or ""
                if rel_props_str:
                    inner_str = rel_props_str.strip("{}").strip()
                    prop_start = query.index(inner_str, query.index(inner_str))
                    top_level, props = parse_prop_str(inner_str, prop_start, rel_top_level_keys)
                else:
                    top_level = {}
                    props = {}

                if "type" in props:
                    props["__type"] = props["type"]
                props["type"] = rel_type

                relationships.append(
                    Relationship(
                        id=rel_id,
                        source=alias_to_id[left_alias],
                        target=alias_to_id[right_alias],
                        **top_level,
                        properties=props,
                    )
                )
            else:
                snippet = part[:30]
                raise ValueError(f"Invalid element in CREATE near: `{snippet}`.")

    return VisualizationGraph(nodes=nodes, relationships=relationships)
