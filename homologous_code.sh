#!/bin/bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh #install conda
bash Miniconda3-latest-Linux-x86_64.sh -b
source ~/.bashrc #re-load your terminal
conda create -y -n biomol python=3.12.9 #create environment
conda activate biomol 
conda install -y -c conda-forge biopython #install biopython (python scrpit requires it)
conda install -y -c bioconda exonerate bedtools  #install exonerate and bedtools

# Setup Conda environment
echo "[INFO] Creating Conda environment..."
conda env create -f environment.yml
conda activate biomol

# Run translation
echo "[INFO] Translating nucleotide sequence..."
python3 dna2protein.py contig_25.fa translated_nucleotide.fa

# Run Exonerate
echo "[INFO] Running Exonerate for exon prediction..."
exonerate -m p2g --showtargetgff -q Arabidopsis_thaliana_prot.fa.txt -t contig_25.fa -S F | \
egrep -w exon > pred_exons_exonerate.gff

# Convert to BED and extract exons
echo "[INFO] Extracting all exon regions..."
awk '$3 == "exon" {print $1"\t"($4-1)"\t"$5"\texon\t.\t"$7}' pred_exons_exonerate.gff > all_exons.bed
bedtools getfasta -fi contig_25.fa -bed all_exons.bed -s -name >  all_exons.fa
#all_exons.fa is our predicted gene sequence
sed -e '2,$s/>.*//'  all_exons.fa | grep -v '^$' > cds_exonerate.txt
#at this point you can compare CDS sequence of both methods

cat cds1_abinitio.fa.txt cds2_abinitio.fa.txt cds_exonerate.txt > cds_comparison.fa

# Translate exons to protein
echo "[INFO] Translating predicted exons..."
python3 dna2protein.py cds_exonerate.txt pred_protein_exonerate.fa

# Merge predictions
echo "[INFO] Merging all predicted proteins..."
cat pred_protein_exonerate.fa ab_initio_proteins.fa.txt > comparison_all.fa

# T-Coffee (optional)
echo "[INFO] You can now upload comparison_all.fa to T-Coffee for alignment."
