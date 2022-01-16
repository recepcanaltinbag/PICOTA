from cycle_finder import parse_gfa, generate_genome_graph
import glob

def best_kmer(kmer_file_loc):

    kmer_files = glob.glob(kmer_file_loc + '/*.py')
    curr_best_file = ""
    curr_best_score = 1
    for file in kmer_files:
        node_dict, edge_dict = parse_gfa(file)
        genome_graph = generate_genome_graph(node_dict, edge_dict)
        deadends = 0
        for node in genome_graph.nodes():
            if len(node.in_edges()) > 0 and len(node.out_edges()) == 0:
                deadends += 1

        curr_score = 1/(len(genome_graph.nodes()*(deadends*2)))
        if curr_score < curr_best_score:
            curr_best_file = file
            curr_best_score = curr_score

    return curr_best_file

