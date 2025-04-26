#!/bin/bash

# Setup Conda environment
echo "[INFO] Creating Conda environment..."
conda env create -f environment.yml
conda activate biomol

# Run translation
echo "[INFO] Translating nucleotide sequence..."
python3 dna2protein.py contig_25.fa translated_nucleotide.fa

# Run Exonerate
echo "[INFO] Running Exonerate for exon prediction..."
exonerate -m p2g --showtargetgff -q Arabidopsis_suecica_prot.fa.txt -t contig_25.fa -S F | \
egrep -w exon > pred_proteins_exonerate.gff

# Convert to BED and extract exons
echo "[INFO] Extracting exon regions..."
awk '$3 == "exon" {print $1"\t"($4-1)"\t"$5"\texon\t.\t"$7}' pred_proteins_exonerate.gff > prediction.bed
bedtools getfasta -fi contig_25.fa -bed prediction.bed -s -name > exons.fa
sed -e '2,$s/>.*//' exons.fa | grep -v '^$' > cds_exonerate.txt

# Translate exons to protein
echo "[INFO] Translating predicted exons..."
python3 dna2protein.py cds_exonerate.txt pred_protein_exonerate.fa

# Merge predictions
echo "[INFO] Merging all predicted proteins..."
cat pred_protein_exonerate.fa ab_initio_proteins.fa.txt > comparison_all.fa

# T-Coffee (optional)
echo "[INFO] You can now upload comparison_all.fa to T-Coffee for alignment."
