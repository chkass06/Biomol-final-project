# import biopython module:
from Bio import SeqIO
# define transcribe function: To convert the DNA string into its corresponding transcribed RNA string we will replace all occurrences of “T” in the DNA string with “U”.
def transcribe(seq):
    rna=""
    for ncl in seq:
        if ncl== "T":
            rna += "U"
        else:
            rna += ncl
    return rna
# define translate function: To translate RNA into protein we will use a codon table and aloop.
def translate(seq):
    codon_table = {
    "UUU" : "F", "CUU" : "L", "AUU" : "I", "GUU" : "V",
    "UUC" : "F", "CUC" : "L", "AUC" : "I", "GUC" : "V",
    "UUA" : "L", "CUA" : "L", "AUA" : "I", "GUA" : "V",
    "UUG" : "L", "CUG" : "L", "AUG" : "M", "GUG" : "V",
    "UCU" : "S", "CCU" : "P", "ACU" : "T", "GCU" : "A",
    "UCC" : "S", "CCC" : "P", "ACC" : "T", "GCC" : "A",
    "UCA" : "S", "CCA" : "P", "ACA" : "T", "GCA" : "A",
    "UCG" : "S", "CCG" : "P", "ACG" : "T", "GCG" : "A",
    "UAU" : "Y", "CAU" : "H", "AAU" : "N", "GAU" : "D",
    "UAC" : "Y", "CAC" : "H", "AAC" : "N", "GAC" : "D",
    "UAA" : "*", "CAA" : "Q", "AAA" : "K", "GAA" : "E",
    "UAG" : "*", "CAG" : "Q", "AAG" : "K", "GAG" : "E",
    "UGU" : "C", "CGU" : "R", "AGU" : "S", "GGU" : "G",
    "UGC" : "C", "CGC" : "R", "AGC" : "S", "GGC" : "G",
    "UGA" : "*", "CGA" : "R", "AGA" : "R", "GGA" : "G",
    "UGG" : "W", "CGG" : "R", "AGG" : "R", "GGG" : "G"
}
    protein = ""

    if len(seq)%3 == 0:
        for i in range(0, len(seq), 3):
            codon = seq[i:i + 3]
            protein+= codon_table[codon]
    return protein


import sys
dna=(sys.argv[1])
out=open(sys.argv[2], 'w')

for seq_record in SeqIO.parse(dna, "fasta"):
    rna=transcribe(seq_record.seq)
    prot=translate(rna)
    print('>%s\n%s\n' % (seq_record.description,prot))
    out.write('>%s\n%s\n' % (seq_record.description,prot))
