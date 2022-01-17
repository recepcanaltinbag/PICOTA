
import subprocess
import os
import glob
from Bio import SeqIO


# ----------------------------------------------------------------
# 1- FILTERING THE RAW FILE WITH SICKLE
# ----------------------------------------------------------------
'''
Usage: sickle se [options] -f <fastq sequence file> -t <quality type> -o <trimmed fastq file>
-f, --fastq-file, Input fastq file (required)
-t, --qual-type, Type of quality values (solexa (CASAVA < 1.3), illumina (CASAVA 1.3 to 1.7), sanger (which is CASAVA >= 1.8)) (required)
-o, --output-file, Output trimmed fastq file (required)
'''
# file path is list
def raw_read_filtering(raw_file, file_end_type, q_type, qual_threshold, out_folder):
    if file_end_type == "se":
        raw_file_1_path = raw_file[0]
        filtered_raw_file_1_name = "filtered_" + raw_file_1_path.split('/')[-1].split('.')[0] 
        f1_path = out_folder + "/" + filtered_raw_file_1_name +".fastq"
        args = f"programs/sickle/sickle se -f {raw_file_1_path} -t {q_type} -q {qual_threshold} -o {f1_path}"
        my_process = subprocess.run(args, shell=True, executable='/bin/bash', text=True, check=True)
        filtering_visualization(raw_file_1_path, out_folder)
        filtering_visualization(f1_path, out_folder)

    elif file_end_type == "pe":
        raw_file_1_path = raw_file[0]
        raw_file_2_path = raw_file[1]
        filtered_raw_file_1_name = "filtered_" + raw_file_1_path.split('/')[-1].split('.')[0]
        filtered_raw_file_2_name = "filtered_" + raw_file_2_path.split('/')[-1].split('.')[0]
        f1_path = out_folder + "/" + filtered_raw_file_1_name +".fastq"
        f2_path = out_folder + "/" + filtered_raw_file_2_name +".fastq"
        s_path = out_folder + "/" + filtered_raw_file_2_name +"s.fastq"
        args = f"programs/sickle/sickle pe -f {raw_file_1_path} -r {raw_file_2_path} \
            -t {q_type} -q {qual_threshold} -o {f1_path} -p {f2_path} -s {s_path}" 
        print(args)
        my_process = subprocess.run(args, shell=True, executable='/bin/bash', text=True, check=True)
        filtering_visualization(raw_file_1_path, out_folder)
        filtering_visualization(f1_path, out_folder)
        filtering_visualization(raw_file_2_path, out_folder)
        filtering_visualization(f2_path, out_folder)
 

# ----------------------------------------------------------------
# 2- FILTERING RESULT VISUALIZATION WIHT FASTQC
# ----------------------------------------------------------------
'''
fastqc seqfile1 seqfile2 .. seqfileN

    fastqc [-o output dir] [--(no)extract] [-f fastq|bam|sam] 
           [-c contaminant file] seqfile1 .. seqfileN

'''
def filtering_visualization(file_path, out_folder):
    args = f"programs/fastqc/fastqc {file_path} -o {out_folder}" 
    my_process = subprocess.run(args, shell=True, executable='/bin/bash', text=True, check=True)
