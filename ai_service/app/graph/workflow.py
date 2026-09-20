from langgraph.graph import END, START, StateGraph

from app.graph.nodes import (
    build_daily_brief_node,
    extract_actions_node,
    group_actions_node,
    resolve_actions_node,
)
from app.graph.state import MeetOpsState


def build_meetops_graph():
    graph = StateGraph(MeetOpsState)

    graph.add_node(
        "extract_actions",
        extract_actions_node,
    )

    graph.add_node(
        "resolve_actions",
        resolve_actions_node,
    )

    graph.add_node(
        "group_actions",
        group_actions_node,
    )

    graph.add_node(
        "build_daily_brief",
        build_daily_brief_node,
    )

    graph.add_edge(
        START,
        "extract_actions",
    )

    graph.add_edge(
        "extract_actions",
        "resolve_actions",
    )

    graph.add_edge(
        "resolve_actions",
        "group_actions",
    )

    graph.add_edge(
        "group_actions",
        "build_daily_brief",
    )

    graph.add_edge(
        "build_daily_brief",
        END,
    )

    return graph.compile()