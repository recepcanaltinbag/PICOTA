import networkx as nx

def reverse_complement(seq):
    complement_dict = {"A":"T", "T":"A", "G":"C", "C":"G", "a":"t", "t":"a", "g":"c", "c":"g"}
    return "".join([complement_dict[nucleotide] for nucleotide in reversed(seq)])


def reverse_sign(sign):
    sign_dict = {"+" : "-", "-" : "+"}
    return sign_dict[sign]


def parse_gfa(path_to_gfa):
    edge_dict = {}
    node_dict = {}
    with open(path_to_gfa, "r") as gfa:

        for line in gfa:

            #Add sequences as nodes, one node for each strand of the DNA
            if line.startswith("S"):
                temp = line.strip("\n").split("\t")
                node_dict[temp[1] + "+"] = {"Name": temp[1] + "+", "Sequence": temp[2]}
                node_dict[temp[1] + "-"] = {"Name": temp[1] + "-", "Sequence": reverse_complement(temp[2])}

            # Add links as edges, one edge for each link. Since two nodes for each sequence exits reverse links are also
            # generated and added as edges.
            elif line.startswith("L"):
                temp = line.strip("\n").split("\t")
                if (temp[1] + temp[2], temp[3] + temp[4]) not in edge_dict.keys() and (
                        temp[3] + reverse_sign(temp[4]), temp[1] + reverse_sign(temp[2])) not in edge_dict.keys():

                    edge_dict[(temp[1] + temp[2], temp[3] + temp[4])] = {"From": temp[1] + temp[2],
                                                                         "To": temp[3] + temp[4], "FromOrient": temp[2],
                                                                         "ToOrient": temp[4], "Overlap": temp[5]}

                    edge_dict[(temp[3] + reverse_sign(temp[4]), temp[1] + reverse_sign(temp[2]))] = {
                        "From": temp[3] + reverse_sign(temp[4]), "To": temp[1] + reverse_sign(temp[2]),
                        "FromOrient": reverse_sign(temp[4]), "ToOrient": reverse_sign(temp[2]), "Overlap": temp[5]}
    return node_dict, edge_dict


def generate_genome_graph(node_dict, edge_dict):

    G = nx.DiGraph()

    #add nodes and edges to the directed graph
    G.add_nodes_from(list(node_dict.keys()))
    nx.set_node_attributes(G, node_dict)

    G.add_edges_from(list(edge_dict.keys()))
    nx.set_edge_attributes(G, edge_dict)

    return G



def reversed_cycle(cycle):
    #same cycle but in the other strand
    return [node[:-1] + reverse_sign(node[-1]) for node in cycle]


def find_nodup_cycles(genome_graph):
    cycles = nx.simple_cycles(genome_graph)
    cycle_nodup = []
    # eliminates cycles that are the same but in the other strand
    for cycle in cycles:
        if set(reversed_cycle(cycle)) not in [set(cycle) for cycle in cycle_nodup]:
            cycle_nodup.append(cycle)
    return cycle_nodup


def cycles_to_fasta(genome_graph, cycles, output="./cycles.fasta", shorter_than=None):

    with open(output, "w") as to_file:
        for cycle in cycles:
            sequence = ""
            length = len(cycle)
            for i in range(len(cycle)):
                overlap = genome_graph.edges[(cycle[i], cycle[(i + 1) % length])]["Overlap"]

                #Since sequences overlap they can not be added back to back, this determines the length of overlap from
                #edge attributes
                if overlap == "*":
                    print(
                        f"At least on of the edges has non-specified overlap in this cycle: {cycle}\n Skipping cycle...")
                    break
                elif overlap == "0M":
                    overlap_length = 0
                else:
                    overlap_length = int(overlap[:-1])

                sequence += genome_graph.nodes[cycle[i]]["Sequence"][:-overlap_length]

            if overlap != "*":
                sequence += genome_graph.nodes[cycle[0]]["Sequence"] + "\n"
                identificator = ">" + "|".join(cycle) + "\n"
                if shorter_than:
                    if len(sequence) < shorter_than:
                        continue
                to_file.write(identificator)
                to_file.write(sequence)

def cycle_finder_driver(path_to_gfa, output="./cycles.fasta", shorter_than=None):

    node_dict, edge_dict = parse_gfa(path_to_gfa)
    genome_graph = generate_genome_graph(node_dict, edge_dict)
    cycles = find_nodup_cycles(genome_graph)
    cycles_to_fasta(genome_graph, cycles, output=output, shorter_than=shorter_than)


if __name__ == "__main__":
    path_to_data = "test_data_P.nitroreducens_1Iinsides.gfa"
    node_dict, edge_dict = parse_gfa(path_to_data)
    genome_graph = generate_genome_graph(node_dict,edge_dict)
    cycles = find_nodup_cycles(genome_graph)
    cycles_to_fasta(genome_graph, cycles)