from Bio import SeqIO
import sys


# Transcription: T → U
def transcribe(seq):
    return seq.upper().replace("T", "U")


# Translation using a manual codon table (RNA codons)
def translate(rna_seq):
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
    rna_seq = rna_seq.upper()
    for i in range(0, len(rna_seq) - 2, 3):
        codon = rna_seq[i:i + 3]
        if len(codon) == 3:
            protein += codon_table.get(codon, "X")  # X = unknown codon
    return protein


# === MAIN EXECUTION ===
if len(sys.argv) != 3:
    print("Usage: python3 dna2prot.py input.fasta output.fasta")
    sys.exit(1)


input_file = sys.argv[1]
output_file = sys.argv[2]


with open(output_file, 'w') as out:
    for record in SeqIO.parse(input_file, "fasta"):
        rna = transcribe(str(record.seq))
        protein = translate(rna)
        out.write(f">{record.description}\n{protein}\n")
        print(f">{record.description}\n{protein}\n")
