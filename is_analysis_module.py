import subprocess
import os
import glob
from Bio import SeqIO
from isescan_parser import parse_driver

# ----------------------------------------------------------------
# 6- INSERTION SEQUENCE FIND
# ----------------------------------------------------------------

'''
isescan.py --seqfile genome1.fa --output results --nthread 2
'''
def insertion_sequence_finder(cycles_file_path, out_folder='IS_Find', threads=2):
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    
    args = f"isescan.py --seqfile {cycles_file_path}  --output {out_folder} --nthread {threads}" 
    my_process = subprocess.run(args, shell=True, executable='/bin/bash', text=True, check=True)

