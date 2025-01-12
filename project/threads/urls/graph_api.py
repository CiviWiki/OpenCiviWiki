from django.urls import path
from threads import graph_api as views

urlpatterns = [
    path("get-graph-data/", views.get_graph_data, name="get-graph-data"),
    path(
        "most-caused-problem/",
        views.get_most_caused_problem,
        name="most-caused-problem",
    ),
    path(
        "most-effective-solution/",
        views.get_most_effective_solution,
        name="most-effective-solution",
    ),
    path(
        "shortest-path/<int:problem_id>/<int:solution_id>/",
        views.get_shortest_path,
        name="shortest-path",
    ),
]
