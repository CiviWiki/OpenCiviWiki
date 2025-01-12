from rest_framework.decorators import api_view
from rest_framework.response import Response
from .graphs import (
    load_graph_from_db,
    most_caused_problems,
    most_effective_solution,
    shortest_path_problem_to_solution,
)


@api_view(["GET"])
def get_most_caused_problem(request):
    with_score = request.GET.get("with_score", False)
    G = load_graph_from_db(with_score)
    problem = most_caused_problems(G)
    if problem:
        if with_score:
            return Response(
                {
                    "problem": G.nodes[problem]["label"],
                    "score": G.nodes[problem]["score"],
                }
            )
        else:
            return Response({"problem": G.nodes[problem]["label"]})
    return Response({"error": "No problem found"}, status=404)


@api_view(["GET"])
def get_most_effective_solution(request):
    with_score = request.GET.get("with_score", False)
    G = load_graph_from_db(with_score)
    solution = most_effective_solution(G)
    if solution:
        if with_score:
            return Response(
                {
                    "solution": G.nodes[solution]["label"],
                    "score": G.nodes[solution]["score"],
                }
            )
        else:
            return Response({"solution": G.nodes[solution]["label"]})
    return Response({"error": "No solution found"}, status=404)


@api_view(["GET"])
def get_shortest_path(request, problem_id, solution_id):
    with_score = request.GET.get("with_score", False)
    G = load_graph_from_db(with_score)
    path = shortest_path_problem_to_solution(G, int(problem_id), int(solution_id))
    if path:
        path_labels = [G.nodes[node]["label"] for node in path]
        return Response({"path_labels": path_labels, "path":path})
    return Response({"error": "No path found"}, status=404)




@api_view(['GET'])
def get_graph_data(request):
    G = load_graph_from_db()  # Load the graph from your DB or other data source
    nodes = []
    edges = []

    # Format nodes and edges to match Cytoscape format
    for node, attr in G.nodes(data=True):
        nodes.append({
            'data': {
                'id': node,
                'label': attr.get('label', node),
                'type': attr.get('type'),
                'score': attr.get('score', 0),
            }
        })

    for source, target, attr in G.edges(data=True):
        edges.append({
            'data': {
                'id': f'{source}-{target}',
                'source': source,
                'target': target,
                'label': attr.get('label', 'related')
            }
        })

    return Response({'nodes': nodes, 'edges': edges})