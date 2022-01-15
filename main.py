import subprocess
import os
import glob
from Bio import SeqIO
from isescan_parser import parse_driver



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
def raw_read_filtering(raw_file, file_end_type, q_type, qual_threshold):
    if file_end_type == "se":
        raw_file_1_path = raw_file[0]
        filtered_raw_file_1_name = "filtered_" + raw_file_1_path.split('/')[-1].split('.')[0] 
        f1_path = "raw_input/" + filtered_raw_file_1_name +".fastq"
        args = f"programs/sickle/sickle se -f {raw_file_1_path} -t {q_type} -q {qual_threshold} -o {f1_path}"
        #my_process = subprocess.run(args, shell=True, executable='/bin/bash', text=True, check=True)
        filtering_visualization(raw_file_1_path)
        filtering_visualization(f1_path)

    elif file_end_type == "pe":
        raw_file_1_path = raw_file[0]
        raw_file_2_path = raw_file[1]
        filtered_raw_file_1_name = "filtered_" + raw_file_1_path.split('/')[-1].split('.')[0]
        filtered_raw_file_2_name = "filtered_" + raw_file_2_path.split('/')[-1].split('.')[0]
        f1_path = "raw_input/" + filtered_raw_file_1_name +".fastq"
        f2_path = "raw_input/" + filtered_raw_file_2_name +".fastq"
        args = f"programs/sickle/sickle pe --pe-file1 {raw_file_1_path} --pe-file2 {raw_file_2_path} \
            --qual-type {q_type} -q {qual_threshold} --output-pe1 {f1_path} --output-pe2 {f2_path}" 
        my_process = subprocess.run(args, shell=True, executable='/bin/bash', text=True, check=True)
        filtering_visualization(raw_file_1_path)
        filtering_visualization(f1_path)
        filtering_visualization(raw_file_2_path)
        filtering_visualization(f2_path)



# ----------------------------------------------------------------
# 2- FILTERING RESULT VISUALIZATION WIHT FASTQC
# ----------------------------------------------------------------
'''
fastqc seqfile1 seqfile2 .. seqfileN

    fastqc [-o output dir] [--(no)extract] [-f fastq|bam|sam] 
           [-c contaminant file] seqfile1 .. seqfileN

'''
def filtering_visualization(file_path):
    args = f"programs/fastqc/fastqc {file_path} -o raw_input" 
    my_process = subprocess.run(args, shell=True, executable='/bin/bash', text=True, check=True)



# ----------------------------------------------------------------
# 3- ASSEMBLY WITH MEGAHIT
# ----------------------------------------------------------------
'''
Usage:
  megahit [options] {-1 <pe1> -2 <pe2> | --12 <pe12> | -r <se>} [-o <out_dir>]

  Input options that can be specified for multiple times (supporting plain text and gz/bz2 extensions)
    -1                       <pe1>          comma-separated list of fasta/q paired-end #1 files, paired with files in <pe2>
    -2                       <pe2>          comma-separated list of fasta/q paired-end #2 files, paired with files in <pe1>
    --12                     <pe12>         comma-separated list of interleaved fasta/q paired-end files
    -r/--read                <se>           comma-separated list of fasta/q single-end files
'''

# file path is list
def assembly_driver(file_path, file_end_type, threads=1):
    if file_end_type == "se":
        args = f"programs/megahit/build/megahit -r {file_path[0]} -o assembly_result/deneme -t {str(threads)} --keep-tmp-files" 
        my_process = subprocess.run(args, shell=True, executable='/bin/bash', text=True, check=True)


def convert_to_fastg_and_gfa(assembly_path):
    fastg_out = assembly_path + '/fastg_files'
    if not os.path.exists(fastg_out):
        os.makedirs(fastg_out)
    gfa_out = 'gfa_files'
    if not os.path.exists(gfa_out):
        os.makedirs(gfa_out)
    
    intermediate_path = assembly_path + "/intermediate_contigs"
    file_list = glob.glob(intermediate_path + '/*.contigs.fa')

    for contig_file in file_list:
        mega_toolkit_driver(contig_file, fastg_out, gfa_out)

    print(file_list)



# ----------------------------------------------------------------
# 4- CONVERSION OF FASTA TO FASTG TO GFA
# ----------------------------------------------------------------
'''
megahit_toolkit contig2fastg 99 k99.contigs.fa > k99.fastg
'''
def mega_toolkit_driver(contig_file, fastg_out, gfa_out):
    kmer_name = contig_file.split('/')[-1].split('.')[0]
    kmer_length = kmer_name.replace('k','')
    fastg_out_path = fastg_out + '/' + kmer_name + '.fastg'
    args = f"programs/megahit/build/megahit_toolkit contig2fastg {kmer_length} {contig_file} > {fastg_out_path}" 
    my_process = subprocess.run(args, shell=True, executable='/bin/bash', text=True, check=True)
    convert_to_gfa(fastg_out_path, gfa_out)
'''
fastg2gfa final.fastg > final.gfa
'''
def convert_to_gfa(fastg_file, gfa_out):
    gfa_name = fastg_file.split('/')[-1].split('.')[0] + '.gfa'
    args = f"programs/fastg2gfa {fastg_file}  > {gfa_out + '/' + gfa_name}" 
    my_process = subprocess.run(args, shell=True, executable='/bin/bash', text=True, check=True)



# ----------------------------------------------------------------
# 5- CYCLE FINDING ALGORITHM
# ----------------------------------------------------------------
'''
Pick best contig_number - deadend ratio file
input = gfa_files/*.gfa  
output = cycles/*.fasta
'''

def cycle_finder():
    return 0




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


# ----------------------------------------------------------------
# 8- ANNOTATION
# ----------------------------------------------------------------
'''
# Choose the names of the output files
% prokka --outdir mydir --prefix mygenome contigs.fa
'''
def annotation_of_result(out_filtered_path, annotation_out):
    if not os.path.exists(annotation_out):
        os.makedirs(annotation_out)
    
    args = f"prokka --outdir {annotation_out} {out_filtered_path}" 
    my_process = subprocess.run(args, shell=True, executable='/bin/bash', text=True, check=True)







# ----------
# ----------
# ----------
# RUNNIG
# ----------
# ----------
# ----------


file_end_type = "se"
q_type = "sanger"
qual_threshold = "30"
raw_file = ["raw_input/SRR639753.fastq"]
#raw_read_filtering(raw_file, file_end_type, q_type, qual_threshold)
#assembly_driver(["raw_input/filtered_SRR639753.fastq"], "se", threads=12)
#convert_to_fastg_and_gfa("assembly_result/deneme")

cycles_file_path = 'cycles/cycles_no1.fasta'
#insertion_sequence_finder(cycles_file_path, threads=12)

# ----------------------------------------------------------------
# 7- PARSING ISESCAN and FILTER THE RESULT
# ----------------------------------------------------------------

IS_result_file = "IS_Find/cycles/cycles_no1.fasta.sum"
out_filtered_path = "filtered_IS_output/filtered_out.fasta"
#parse_driver(IS_result_file, cycles_file_path, out_filtered_path)

# ----------------------------------------------------------------
# 8- ANNOTATION
# ----------------------------------------------------------------
annotation_out = 'annotation' 
annotation_of_result(out_filtered_path, annotation_out)








