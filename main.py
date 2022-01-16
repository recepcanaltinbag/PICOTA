import subprocess
import os
import glob
from Bio import SeqIO
from isescan_parser import parse_driver
from quality_control_module import raw_read_filtering
from assembly_module import assembly_driver

from is_analysis_module import insertion_sequence_finder
from annotation module import *




# ----------------------------------------------------------------
# FILTERING AND ASSEMBLY
# ----------------------------------------------------------------
out_folder = "output"
if not os.path.exists(out_folder):
        os.makedirs(out_folder)
file_end_type = "se"
q_type = "sanger"
qual_threshold = "30"
raw_file = ["raw_input/SRR639753.fastq"] #raw file is list
out_folder_for_filtering = output + '/filtering'
if not os.path.exists(out_folder_for_filtering):
        os.makedirs(out_folder_for_filtering)
raw_read_filtering(raw_file, file_end_type, q_type, qual_threshold, out_folder_for_filtering)
out_folder_for_assembly = output + '/assembly'
assembly_driver(raw_file, "se", threads=12, out_folder_for_assembly)
# (file_path, file_end_type, threads=1, out_folder, k_list = [])
# k_list = [] is optional argument user can select wanted k-mers, only odd numbers


# ----------------------------------------------------------------
# FILTERING AND ASSEMBLY
# ----------------------------------------------------------------


# ----------------------------------------------------------------
# 7- PARSING ISESCAN and FILTER THE RESULT
# ----------------------------------------------------------------
cycles_file_path =  out_folder + '/cycles/cycles_no1.fasta'
threads = 2
out_folder_for_IS = out_folder + '/IS_Find'
insertion_sequence_finder(cycles_file_path, out_folder= out_folder_for_IS, threads=threads)
IS_result_file = out_folder_for_IS + "/" + cycles_file_path + ".sum"
out_filtered_path = out_folder + "/filtered_out.fasta"
parse_driver(IS_result_file, cycles_file_path, out_filtered_path)




# ----------------------------------------------------------------
# 8- ANNOTATION
# ----------------------------------------------------------------
annotation_out = out_folder + '/annotation'
annotation_driver(out_filtered_path, annotation_out)




# ----------------------------------------------------------------
# 8- ANNOTATION for NOVELTY SEARCH
# ----------------------------------------------------------------

out_novel_path = out_folder + '/novel'
if not os.path.exists(out_novel_path):
        os.makedirs(out_novel_path)

annotation_driver_for_novelty(IS_result_file, cycle_file, out_novel_path, annotation_out)







