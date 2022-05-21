import matplotlib.pyplot as plt
from parse_paths import *
from main import split_one_many
# from main import split_one_set_of_paths


def plot_degrees_of_vertexes(vertexes):
    degrees_of_vertexes = [0] * 1000
    for v in vertexes.values():
        degrees_of_vertexes[(len(v.in_vertexes) +
                             len(v.out_vertexes))] += 1
    plt.plot(degrees_of_vertexes)
    plt.xlim(0, 7)
    plt.show()

def plot_coverage(edges):
    cnt = [0] * 1000
    for e in edges.values():
        cnt[len(e.reads)] += 1
    plt.plot(cnt)
    plt.xlim(0, 100)
    plt.show()

def make_analisys():
    file = "final_dbg.gfa"
    graph = run_extraction(file)
    graph = parse_als(graph, "paths.als")

    plot_degrees_of_vertexes(graph.vertexes)
    plot_coverage(graph.edges)


# print("Total vertexes:", len(vertexes.keys()))
# print("Total edges:", len(edges.keys()))
#
# plot_degrees_of_vertexes(vertexes)
#
# print("-- One-to-many-split --")
#
# vertexes, edges = split_one_many(vertexes, edges)
# print("Total vertexes:", len(vertexes.keys()))
# print("Total edges:", len(edges.keys()))
#
# plot_degrees_of_vertexes(vertexes)
#
# print("-- One-set-of-paths-split --")
#
# v_keys = list(vertexes.keys()).copy()
# for v_id in v_keys:
#     vertexes, edges = split_one_set_of_paths(v_id, vertexes, edges)
# print("Total vertexes:", len(vertexes.keys()))
# print("Total edges:", len(edges.keys()))
#
# plot_degrees_of_vertexes(vertexes)
#
#
# for v in vertexes.values():
#     if len(v.in_vertexes) + len(v.out_vertexes) == 2:
#         print(v.id)
#         print(v.in_vertexes, v.out_vertexes)
#         print("in: ")
#         for e_id in v.in_vertexes:
#             print(edges[(e_id, v.id)].reads)
#         print("out: ")
#         for e_id in v.out_vertexes:
#             print(edges[(v.id, e_id)].reads)
#         print()