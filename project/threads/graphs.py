import networkx as nx
from .models import Civi, CiviLink


def load_graph_from_db(with_score:bool=False):
    # Create a directed graph
    G = nx.DiGraph()

    # Add all Civis as nodes
    for civi in Civi.objects.all():
        node_args, node_kwargs = civi.__node__(with_score=with_score)
        G.add_node(*node_args, **node_kwargs)

    # Add CiviLinks as edges
    for link in CiviLink.objects.all():
        edge_args, edge_kwargs = link.__edge__()
        G.add_edge(*edge_args, **edge_kwargs)

    return G


def most_caused_problems(G, with_score:bool=False):
    problem_nodes = [n for n, attr in G.nodes(data=True) if attr["type"] == "Problem"]
    if with_score:
      return max(problem_nodes, key=lambda n: (G.in_degree(n), G.nodes[n]['score']), default=None)
    return max(problem_nodes, key=lambda n: G.in_degree(n), default=None)


def most_effective_solution(G, with_score:bool=False):
    solution_nodes = [n for n, attr in G.nodes(data=True) if attr["type"] == "Solution"]
    if with_score:
      return max(solution_nodes, key=lambda n: (G.out_degree(n), G.nodes[n]['score']), default=None)
    return max(solution_nodes, key=lambda n: G.out_degree(n), default=None)


def shortest_path_problem_to_solution(G, problem_id, solution_id, with_score:bool=False):
    try:
        if with_score:
          return nx.shortest_path(G, source=problem_id, target=solution_id, weight='weight')
        return nx.shortest_path(G, source=problem_id, target=solution_id)
    except nx.NetworkXNoPath:
        return None
