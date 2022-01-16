import subprocess
import os
import glob
import argparse
from Bio import SeqIO
from isescan_parser import parse_driver
from quality_control_module import raw_read_filtering
from assembly_module import assembly_driver
from cycle_finder import cycle_finder_driver
from kmer_choser import best_kmer
from is_analysis_module import insertion_sequence_finder
from annotation module import *
from datetime import datetime

td = datetime.now()
dt_string = td.strftime("%d-%m-%Y-%H-%M-%S")

parser = argparse.ArgumentParser(description='PICOTA: Composite Transposon Finder')
parser.add_argument('rawreads', nargs="+", type=str, help='Path to raw reads')
parser.add_argument('rtype', choices=['se', 'pe'], help='Type of reads: se for single end, pe for paired end')
parser.add_argument('qtype', choices=['sanger', 'illumina', 'solexa'], help='Quality control type: sanger, illumina or solexa')
parser.add_argument('--output', '-o' ,default=dt_string, help='Main output file for the run')
parser.add_argument('--qthreshold', '-q' ,default="30", help='Quality threshold')
parser.add_argument('--ilengthfilter', '-t' ,default=None, type=int, help='Length filter for finding all cycles')
parser.add_argument('--outfiltering', '-f', default='/filtering', help='Output file for filtering')
parser.add_argument('--outassembly', '-a', default='/assembly', help='Output file for assembly')
parser.add_argument('--outcycles', '-c', default='/cycles', help='Output file for cycles')
parser.add_argument('--cyclefasta', '-s', default='cycles_no1.fasta', help='Output fasta file for cycles')
parser.add_argument('--threads', '-t', default=2, type=int, help='Main output file for the run')
parser.add_argument('--outis', '-i', default='/IS_Find', help='Output file for IS_Finder')
parser.add_argument('--outfiltered', '-f', default='"filtered_out.fasta', help='Output file for filtered cycles')
parser.add_argument('--outannotation', '-k', default='/annotation', help='Output file for annotations')
parser.add_argument('--outnovel', '-n', default='/novel', help='Output file for novel transposons')
parser.add_argument('--klist', '-k' ,default=[], nargs="+", type=int, help='Number of kmers to run')
args = parser.parse_args()

# ----------------------------------------------------------------
# FILTERING AND ASSEMBLY
# ----------------------------------------------------------------
out_folder = args.output #USER-general_out_folder_for_the_run ++
if not os.path.exists(out_folder):
        os.makedirs(out_folder)
file_end_type = args.rtype #USER-(required) single_end se paired_end pe ++
q_type = args.qtype #USER-(required) quality type of the fastq file (sanger, illumina, solexa) ++
qual_threshold = args.qthreshold #USER-quality-threshold ++
raw_file = args.rawreads #USER-(required)-a list of raw files, for sinle end file it is only one element, for paired end two elements+
out_folder_for_filtering = out_folder + args.outfiltering #USER-(can be optional) +
if not os.path.exists(out_folder_for_filtering):
        os.makedirs(out_folder_for_filtering)
raw_read_filtering(raw_file, file_end_type, q_type, qual_threshold, out_folder_for_filtering)
out_folder_for_assembly = out_folder + args.outassembly #USER-(can be optional) ++
k_list = args.klist #USER-(optional) ++
# k_list = [] is optional argument user can select wanted k-mers, only odd numbers

assembly_driver(raw_file, file_end_type, out_folder_for_assembly, threads=12, k_list=k_list)


# ----------------------------------------------------------------
# FILTERING AND ASSEMBLY
# ----------------------------------------------------------------
best_kmer_file = kmer_choser(out_folder_for_assembly)
cycles_file_path =  out_folder + args.outcycles #USER-(can be optional or given by the system) ++
if not os.path.exists(cycles_file_path):
        os.makedirs(cycles_file_path)
cycles_fasta = args.cyclefasta 
cycles_file_path = cycles_file_path + cycles_fasta
initial_length_filter = args.ilengthfilter
cycle_finder_driver(best_kmer_file, output=cycles_file_path, shorter_than=initial_length_filter)

# ----------------------------------------------------------------
# 7- PARSING ISESCAN and FILTER THE RESULT
# ----------------------------------------------------------------

threads = args.threads #USER-(can be optional) ++
out_folder_for_IS = out_folder + args.outis #USER-(can be optional or given by the system) ++
insertion_sequence_finder(cycles_file_path, out_folder= out_folder_for_IS, threads=threads)
IS_result_file = out_folder_for_IS + "/" + cycles_file_path + ".sum"   #USER-(can be optional or given by the system) -
out_filtered_path = out_folder + args.outfiltered #USER-(can be optional or given by the system) ++
parse_driver(IS_result_file, cycles_file_path, out_filtered_path)


# ----------------------------------------------------------------
# 8- ANNOTATION
# ----------------------------------------------------------------
annotation_out = out_folder + args.outannotation #USER-(can be optional or given by the system) ++
annotation_driver(out_filtered_path, annotation_out)  




# ----------------------------------------------------------------
# 8- ANNOTATION for NOVELTY SEARCH
# ----------------------------------------------------------------

out_novel_path = out_folder + args.outnovel  #USER-(can be optional or given by the system) ++
if not os.path.exists(out_novel_path):
        os.makedirs(out_novel_path)

annotation_driver_for_novelty(IS_result_file, cycle_file, out_novel_path, annotation_out)







