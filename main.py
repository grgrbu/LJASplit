from parse_paths import *
from analytics import *

# def print_in_out(vertexes):
#     for vertex_id in vertexes.keys():
#         v = vertexes[vertex_id]
#         if (len(v.in_vertexes) + len(v.out_vertexes)) == 4:
#             print(vertexes[vertex_id].id)
#             print(vertexes[vertex_id].in_vertexes)
#             print(vertexes[vertex_id].out_vertexes)

def split_one_many(graph):
    vertexes_at_start = list(graph.vertexes.keys())
    cnt = 0
    for vertex_id in vertexes_at_start:
        print("cnt = ", cnt)
        print("vertex_id:", vertex_id)
        if cnt > 3:
            return graph
        v = graph.vertexes[vertex_id]
        if len(v.in_vertexes) == 1 and len(v.out_vertexes) > 1:
            cnt += 1
            in_ed_id = v.in_vertexes[0]
            outs_v_ind = v.out_vertexes
            reads_through_in = graph.edges[in_ed_id].reads

            print("edge label:", graph.edges[in_ed_id].label)
            print("edge:", in_ed_id)
            print("outs_v_ind: ", outs_v_ind)


            v_from = graph.vertexes[graph.edges[in_ed_id].from_v]
            print("to:", graph.vertexes[graph.edges[in_ed_id].to_v])
            print(graph.vertexes)
            print(graph.edges)
            for i in range(len(outs_v_ind)):
                new_vertex_id = max(graph.vertexes.keys()) + 1
                graph.vertexes[new_vertex_id] = Vertex(new_vertex_id)
                new_vertex = graph.vertexes[new_vertex_id]

                out_ed_id = outs_v_ind[i]
                new_vertex.out_vertexes.append(out_ed_id)
                graph.edges[out_ed_id].from_v = new_vertex.id

                graph.print_to_gfa("check_short_" + str(cnt) + "added_new_v" + str(i) + ".gfa")

                print(v_from.id, new_vertex.id)
                graph.AddEdge(v_from.id,
                              new_vertex.id,
                              graph.edges[in_ed_id].seq, reads_through_in,
                              graph.edges[in_ed_id].label[:-1]+"88"+str(i)+graph.edges[in_ed_id].label[-1])

                print(graph.vertexes)
                print(graph.edges)

            graph.InternalRemoveEdge(in_ed_id)
            graph.vertexes.pop(v.id)
            print(graph.vertexes)
            print(graph.edges)

            graph.print_to_gfa("check_short_" + str(cnt) + ".gfa")
        print()
        break

    print("split one-many", cnt, "vertexes")
    print(graph.vertexes)
    print(graph.edges)
    return graph


# def split_one_set_of_paths(v_id, vertexes, edges):
#     v = vertexes[v_id]
#     if len(v.in_vertexes) < 2 or len(v.out_vertexes) < 2:
#         return vertexes, edges
#
#     for in_v in v.in_vertexes:
#         for out_v in v.out_vertexes:
#             no_other = True
#             reads_through_pair = edges[(in_v, v.id)].reads & edges[(v.id, out_v)].reads
#             if len(reads_through_pair) == 0:
#                 continue
#             for in_v2 in v.in_vertexes:
#                 if in_v2 == in_v:
#                     continue
#                 for out_v2 in v.out_vertexes:
#                     if out_v2 == out_v:
#                         continue
#                     reads_through_pair2 = edges[(in_v2, v.id)].reads & edges[(v.id, out_v2)].reads
#                     if len(reads_through_pair & reads_through_pair2) >= 1:
#                         no_other = False
#             if no_other:
#                 new_vertex_id = v.id + "_copy_osp"
#                 vertexes[new_vertex_id] = Vertex(new_vertex_id)
#
#                 vertexes[new_vertex_id].in_vertexes.add(in_v)
#                 vertexes[in_v].out_vertexes.add(new_vertex_id)
#
#                 vertexes[new_vertex_id].out_vertexes.add(out_v)
#                 vertexes[out_v].in_vertexes.add(new_vertex_id)
#
#                 edges[(in_v, new_vertex_id)] = Edge(reads_through_pair, in_v, new_vertex_id)
#                 edges[(new_vertex_id, out_v)] = Edge(reads_through_pair, new_vertex_id, out_v)
#
#                 v.in_vertexes.remove(in_v)
#                 vertexes[in_v].out_vertexes.remove(v.id)
#                 v.out_vertexes.remove(out_v)
#                 vertexes[out_v].in_vertexes.remove(v.id)
#
#                 edges.pop((in_v, v.id))
#                 edges.pop((v.id, out_v))
#                 return vertexes, edges

#     return vertexes, edges


if __name__ == '__main__':

    # f = open("check_overlap.txt", "r")
    # a = f.readline()[:-1]
    # b = f.readline()
    # print(intersect_two_strings(a, b))
    # print(a[-3:])

    # print(graph.vertexes)
    # print(graph.edges)
    # print(graph.edges.keys())
    # print(graph.edges[135907690340893512010980773524720261933100*2+1])

    # for egde in graph.edges.values():
    #     print(egde.reads)


    # print(graph.edges)
    # print(graph.vertexes)

    file = "./short.gfa"
    graph = run_extraction(file)
    graph = parse_als(graph, "./paths_short.als")
    graph.print_to_gfa("short_check.gfa")

    graph = split_one_many(graph)
    print("!")

    # plot_degrees_of_vertexes(graph.vertexes)

    # graph.print_to_gfa("check.gfa")
    # plot_degrees_of_vertexes(graph.vertexes)
    # print(graph.edges.keys())
    # get_paths_through_edge(graph, "1735780502544106241390669741398093458311G")
#

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
