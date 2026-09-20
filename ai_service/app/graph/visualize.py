from app.graph.workflow import build_meetops_graph


def print_graph():
    graph = build_meetops_graph()

    print(graph.get_graph().draw_ascii())


if __name__ == "__main__":
    print_graph()