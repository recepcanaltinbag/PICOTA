
from Bio import SeqIO


def parse_IS_result_file(file_read): 
    file_lines = file_read.readlines()
    if len(file_lines) > 2:
        file_lines.pop(-1)
        file_lines.pop(0)
        return file_lines
    else:
        print('Empty result file, ttry again')
        return False


def parse_driver(IS_result_file, cycle_file, out_filtered_path):
    file_read = open(IS_result_file,'r')
    file_lines = parse_IS_result_file(file_read)

    if file_lines != False:
        seq_list = []
        for line in file_lines:
            seq_id = line.split(' ')[0]
            if seq_id not in seq_list:
                seq_list.append(seq_id)

        filtered_fasta = ""
        with open(cycle_file) as handle:
            for record in SeqIO.parse(handle, "fasta"):
                
                if record.id in seq_list:
                    filtered_fasta = filtered_fasta + '>' + str(record.id) + '\n' + str(record.seq) + '\n'


        out_filtered_file = open(out_filtered_path,"w")
        out_filtered_file.write(filtered_fasta)




