# a significant part of the code in this file is taken from
# https://github.com/AntonBankevich/LJA/blob/trio_wip2/src/projects/scripts/trio/extract_unbranching_paths.py

from vertex import Vertex
from edge import Edge
from Bio.Seq import Seq

def intersect_two_strings(s, t):
    ans = 0
    for i in range(len(t) - 1, -1, -1):
        M = i + 1
        if s[-M:] == t[:M]:
            ans = M
            break
    return t[:ans]

class Graph:
    vertexes = dict()
    edges = dict()

    def __init__(self, vertexes, edges):
        self.vertexes = vertexes
        self.edges = edges
        self.vs_to_e = dict()
        self.edge_next_id = max(edges.keys()) + 1

    def AddEdge(self, start_vertex, end_vertex, new_seq, reads, new_label):
        eid = self.edge_next_id
        self.edges[eid] = Edge(eid, start_vertex, end_vertex, new_seq)
        self.edges[eid].label = new_label
        self.edges[eid].reads = reads
        self.vertexes[start_vertex].in_vertexes.append(eid)
        self.vertexes[end_vertex].out_vertexes.append(eid)
        self.edge_next_id += 1

    def InternalRemoveEdge(self, eid):
        incident = [self.edges[eid].from_v, self.edges[eid].to_v]
        for vid in incident:
            if eid in self.vertexes[vid].in_vertexes:
                self.vertexes[vid].in_vertexes.remove(eid)
            if eid in self.vertexes[vid].out_vertexes:
                self.vertexes[vid].out_vertexes.remove(eid)
        del self.edges[eid]


    def print_to_gfa(self, outfile):
        labels = {}
        canonic = {}
        out_f = open(outfile, 'w')

        for e in self.edges.keys():
            if not (e in labels):
                dirty_label = self.edges[e].label.replace("+", "P").replace("-", "M")
                out_f.write(f'S\t{dirty_label}\t{self.edges[e].seq}\n')
                labels[e] = dirty_label
                canonic[e] = True
                labels[self.edges[e].get_rc_id()] = dirty_label
                canonic[self.edges[e].get_rc_id()] = False
        for vid in self.vertexes.keys():
            if self.vertexes[vid].rc_id < vid:
                print(self.vertexes[vid].id)
                continue
            for eid in self.vertexes[vid].in_vertexes:
                inc_label = "+"
                if canonic[eid] == False:
                    inc_label = "-"
                for out_eid in self.vertexes[vid].out_vertexes:
                    out_label = "+"
                    if canonic[out_eid] == False:
                        out_label = "-"
                    out_f.write(
                        f'L\t{labels[eid]}\t{inc_label}\t{labels[out_eid]}\t{out_label}\t{self.vertexes[vid].k}M\n')


class node_stat:
    def __init__(self, length, cov, seq):
        self.length = int(length)
        self.cov = float(cov)
        self.seq = seq


def get_ids(link_name):
    arr = link_name.split()
    res = [change_e_id(arr[1]), change_e_id(arr[3])]
    return res


def rc(seq):
    seqS = Seq(seq)

    return seqS.reverse_complement().__str__()


def construct_graph(edge_component, segments, links):
    vertices = {}
    equivalents = {}
    canonic_ids = {}
    id_count = 0
    edge_count = 0
    edges_to_id = {}
    edges = {}
    vs_to_e = dict()
    for e in edge_component:
        e_str = e
        e = int(e)
        # starts, end, rc_start, rc_end   0,1,2,3, rc_id = 3 - id
        for i in range(0, 4):
            vertices[id_count] = Vertex(id_count)
            equivalents[id_count] = set({id_count})
            id_count += 1
        edges_to_id[e] = edge_count
        vertices[edge_count * 4].out_vertexes.append(e * 2)
        vertices[edge_count * 4 + 2].out_vertexes.append(e * 2 + 1)
        vertices[edge_count * 4 + 1].in_vertexes.append(e * 2)
        vertices[edge_count * 4 + 3].in_vertexes.append(e * 2 + 1)
        edges[e * 2] = Edge(e * 2, edge_count * 4, edge_count * 4 + 1, segments[e_str].seq)
        vs_to_e[(edge_count * 4, edge_count * 4 + 1)] = e * 2
        edges[e * 2 + 1] = Edge(e * 2 + 1, edge_count * 4 + 2, edge_count * 4 + 3, rc(segments[e_str].seq))
        vs_to_e[(edge_count * 4 + 2, edge_count * 4 + 3)] = e * 2 + 1
        edge_count += 1

    # print(edges_to_id)
    # adding edges from lines
    for e in edge_component:
        if e not in links:
            continue
        for l in links[e]:
            arr = l.split()
            # L	edge_43116	-	edge_6653	+	0M

            edge_start = e
            edge_end = arr[3]
            first_edge = int(edge_start) * 2
            second_edge = int(edge_end) * 2
            overlap = int(arr[5][:-1])
            link_start_shift = 1
            if arr[2] == '-':
                first_edge += 1
            link_end_shift = 0
            if arr[4] == '-':
                second_edge += 1

            start_id = edges[first_edge].to_v
            end_id = edges[second_edge].from_v
            #            print (f'from link {l} adding edge {start_id} {end_id} ')
            #            vertices[start_id].next.append(end_id)
            #            vertices[end_id].prev.append(start_id)
            equivalents[start_id].update(equivalents[end_id])
            for tmp in equivalents[start_id]:
                if tmp != start_id:
                    equivalents[tmp].update(equivalents[start_id])
            vertices[start_id].k = overlap
            vertices[end_id].k = overlap
            # rc_Link
            start_id = vertices[start_id].rc_id
            end_id = vertices[end_id].rc_id
            #            print(f'from link {l} adding edge {end_id} {start_id} ')
            #            vertices[end_id].next.append(start_id)
            #            vertices[start_id].prev.append(end_id)
            equivalents[start_id].update(equivalents[end_id])
            for tmp in equivalents[start_id]:
                if tmp != start_id:
                    equivalents[tmp].update(equivalents[start_id])

            vertices[start_id].k = overlap
            vertices[end_id].k = overlap
    for v in vertices.keys():
        canonic_ids[v] = v
        for w in equivalents[v]:
            if w < canonic_ids[v]:
                canonic_ids[v] = w
    canonic_vertices = {}
    for v in vertices.keys():
        if canonic_ids[v] == v:
            canonic_vertices[v] = Vertex(v)
            canonic_vertices[v].rc_id = canonic_ids[vertices[v].rc_id]
            canonic_vertices[v].k = vertices[v].k
    # canonic ids is smallest between all equivalents, so it exists
    for v in vertices.keys():
        #        print(f'{v}  {len(vertices[v].outgoing)} {len(vertices[v].incoming)}')
        for i in vertices[v].out_vertexes:
            #            print(f'  {i}')
            canonic_vertices[canonic_ids[v]].out_vertexes.append(i)
        for i in vertices[v].in_vertexes:
            #            print(f'  {i}')
            canonic_vertices[canonic_ids[v]].in_vertexes.append(i)
    #    for v in canonic_vertices.keys():
    #        print(canonic_vertices[v])
    for id in edges.keys():
        edges[id].from_v = canonic_ids[edges[id].from_v]
        edges[id].to_v = canonic_ids[edges[id].to_v]
        vs_to_e[(canonic_ids[edges[id].from_v], canonic_ids[edges[id].to_v])] = id
    #        print(edges[id])
    G = Graph(canonic_vertices, edges)
    G.vs_to_e = vs_to_e
    # print(G.vs_to_e)
    return G


def change_e_id(e_id):
    # to turn id into number
    dict_ch = dict()
    dict_ch["A"] = "04"
    dict_ch["C"] = "00"
    dict_ch["G"] = "06"
    dict_ch["T"] = "01"
    return  e_id[:-1] + dict_ch[e_id[-1]]


def run_extraction(graph_f):
    neighbours = {}
    segments = {}
    links = {}

    for line in open(graph_f, 'r'):
        if line[0] == "L":
            arr = get_ids(line)
            if len(arr) <= 1:
                print(line)
                exit()
            if not (arr[0] in neighbours.keys()):
                neighbours[arr[0]] = set()
            if not (arr[1] in neighbours.keys()):
                neighbours[arr[1]] = set()
            neighbours[arr[0]].add(arr[1])
            neighbours[arr[1]].add(arr[0])
            if not arr[0] in links:
                links[arr[0]] = []
            if not arr[1] in links:
                links[arr[1]] = []

            full_arr = line.split()
            full_arr[1], full_arr[3] = change_e_id(full_arr[1]), change_e_id(full_arr[3])
            links[arr[0]].append(" ".join(full_arr))

        elif line[0] == "S":
            arr = line.split()
            arr[1] = change_e_id(arr[1])
            length = len(arr[2])
            #            cov = arr[3].split(':')[2]
            cov = 1
            segments[arr[1]] = node_stat(length, cov, arr[2])
            neighbours[arr[1]] = set()

    graph = construct_graph(segments.keys(), segments, links)
    return graph

def get_paths_through_edge(graph, e):
    print(graph.edges[change_e_id(e)].reads)
