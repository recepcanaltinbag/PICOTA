import subprocess
import os
import glob
from Bio import SeqIO
from isescan_parser import parse_driver
from isescan_parser import parse_novel_driver

# ----------------------------------------------------------------
# 8- ANNOTATION
# ----------------------------------------------------------------
'''
# Choose the names of the output files
% prokka --outdir mydir --prefix mygenome contigs.fa
'''
def annotation_driver(out_filtered_path, annotation_out):
    if not os.path.exists(annotation_out):
        os.makedirs(annotation_out)
    
    args = f"prokka --outdir {annotation_out} {out_filtered_path}" 
    my_process = subprocess.run(args, shell=True, executable='/bin/bash', text=True, check=True)
   
  
  
def annotation_driver_for_novelty(IS_result_file, cycle_file, out_novel_path, annotation_out):
    parse_novel_driver(IS_result_file, cycle_file, out_novel_path)
    
    if not os.path.exists(annotation_out):
        os.makedirs(annotation_out)
    
    args = f"prokka --outdir {annotation_out} {out_novel_path}" 
    my_process = subprocess.run(args, shell=True, executable='/bin/bash', text=True, check=True)
