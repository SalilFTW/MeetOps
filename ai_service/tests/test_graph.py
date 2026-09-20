from app.graph.runner import run_meetops_agent
from app.graph.workflow import build_meetops_graph


def test_meetops_graph_builds():
    graph = build_meetops_graph()

    assert graph is not None


def test_meetops_graph_deterministic_execution():
    result = run_meetops_agent(use_llm=False)

    assert result is not None
    assert "canonical_actions" in result
    assert "my_actions" in result
    assert "waiting_on_others" in result
    assert "unclear_actions" in result


def test_meetops_graph_contains_actions():
    result = run_meetops_agent(use_llm=False)

    canonical_actions = result["canonical_actions"]

    assert len(canonical_actions) > 0


def test_meetops_graph_groups_actions():
    result = run_meetops_agent(use_llm=False)

    assert len(result["my_actions"]) > 0
    assert len(result["waiting_on_others"]) > 0
    assert len(result["unclear_actions"]) > 0