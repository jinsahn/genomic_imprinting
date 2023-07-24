#!/bin/bash
mkdir -p fimo_out
for i in *.meme; do
fimo --oc fimo_out_${i%.meme} --verbosity 1 --bfile --motif-- --thresh 1.0E-4 \
--parse-genomic-coord $i \
All_-2000TSS_+1000TSS_KBTBD6.fa

mv fimo_out_* fimo_out
grep -v '^#\|^$' fimo_out/fimo_out_${i%.meme}/fimo.tsv > fimo_out/fimo_out_${i%.meme}/fimo_clean.tsv

done

# concatenate
for file in fimo_out/fimo_out_*/fimo_clean.tsv
do
    cat "$file" >> fimo_combined_results.tsv
done

# remove header in between motifs
grep -v '^motif_id' fimo_combined_results.tsv > fimo_combined_results_no_header.tsv

# add header for the 1st row.
printf "motif_id\tmotif_alt_id\tsequence_name\tstart\tstop\tstrand\tscore\tp-value\tq-value\tmatched_sequence\n" > header.tsv
cat header.tsv fimo_combined_results_no_header.tsv > fimo_combined_results.tsv
