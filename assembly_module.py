import subprocess
import os
import glob
from Bio import SeqIO

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
    --k-list                 <int,int,..>   comma-separated list of kmer size
                                            all must be odd, in the range 15-255, increment <= 28)
                                            [21,29,39,59,79,99,119,141]

'''

# file path is list
def assembly_driver(file_path, file_end_type,  out_folder, threads=1,k_list = []):
    if k_list == []:
      k_mer_value = ''
    else:
      k_mer_value = '--k-list' + ','.join(k_list)
    
    if file_end_type == "se":
        args = f"programs/megahit/build/megahit -r {file_path[0]} -o {out_folder} -t {str(threads)} --keep-tmp-files {k_mer_value}" 
        my_process = subprocess.run(args, shell=True, executable='/bin/bash', text=True, check=True)
    elif file_end_type == "pe":
        args = f"programs/megahit/build/megahit -1 {file_path[0]} -2 {file_path[1]} -o {out_folder} -t {str(threads)} --keep-tmp-files {k_mer_value}" 
        my_process = subprocess.run(args, shell=True, executable='/bin/bash', text=True, check=True)
    
    convert_to_fastg_and_gfa(out_folder)
    
    
    
def convert_to_fastg_and_gfa(assembly_path):
    fastg_out = assembly_path + '/fastg_files'
    if not os.path.exists(fastg_out):
        os.makedirs(fastg_out)
    gfa_out = assembly_path + '/gfa_files'
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

