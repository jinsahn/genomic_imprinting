import subprocess
import os

# Update PATH for samtools and MethylDackel
home_path = os.environ["HOME"]
os.environ["PATH"] = f"{home_path}/local/samtools-1.11:{home_path}/local:{os.environ['PATH']}"

def run_command(command):
    result = subprocess.run(command, shell=True, check=True, text=True)
    return result

fasta_path = "/path/to/fasta/file"

for i in [10, 11]:
    input_bam = f"SRR{i}_1_val_1_bismark_bt2_pe.deduplicated_chr11.sorted.bam"
    output_bam = f"SRR{i}_1_val_1_bismark_bt2_pe.deduplicated_chr11_25705500-25706700.bam"
    methyldackel_output = f"SRR{i}_1_val_1_bismark_bt2_pe.deduplicated_chr11_25705500-25706700_MethylDackel.txt"

    # subset bam
    samtools_command = f"samtools view -b {input_bam} chr11:25705500-25706700 > {output_bam}"
    run_command(samtools_command)
    
    # extract reads
    methyldackel_command = f"MethylDackel perRead {fasta_path} {output_bam} -o {methyldackel_output}"
    run_command(methyldackel_command)
    
    # Add header to the txt and rename
    header = "readname\tchr\tstart\tmetperc\tnoCpG"
    with open(methyldackel_output, 'r') as original_file:
        content = original_file.read()
    
    with open(methyldackel_output, 'w') as modified_file:
        modified_file.write(header + '\n' + content)

print("succeed!")