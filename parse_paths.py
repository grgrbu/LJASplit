from vertex import Vertex
from edge import Edge
from graph import *

# f = open("./paths.als", "r")
# f = open("./paths_short.als", "r")

def parse_als(graph, file):
    f = open(file, "r")

    while True:
        line_read_id = f.readline()
        line_vecsize = f.readline()
        line_type = f.readline()
        line_path = f.readline()
        if not line_path:
            break

        read_id = line_read_id.split()[1]

        path = line_path.split()[1::2]
        path_length = len(path)

        if path_length == 1:
            continue

        for i in range(path_length):
            e_id = int(change_e_id(path[i]))
            # print(e_id*2)
            if e_id * 2 in graph.edges.keys():
                graph.edges[e_id*2].reads.add(read_id)
                graph.edges[e_id*2+1].reads.add(read_id)

    print("parsed paths successfully")
    return graph


# print(len(vertexes))
# print(edges)
