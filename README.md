# 🧬 Homology-Based Gene Prediction Code

This repository contains a full pipeline for performing **gene prediction** based on **homology to known protein sequences**, particularly across species within the *Arabidopsis* genus. The goal is to identify **protein-coding genes (exons)** in an unannotated genomic DNA sequence using both **sequence alignment tools** and **biological inference**.

---

## 📘 Project Overview

When working with a newly sequenced genome or an unknown DNA fragment, identifying coding regions (genes) can be challenging. 
In this part of the project we'll be using an **homology-based gene prediction**, which relies on **comparing the unknown DNA to known, annotated proteins from related species**. 

By aligning known protein sequences to our input DNA, we can infer where exons are likely located, even without direct annotation. 
We also incorporate **ab initio** predictions for comparison, ensuring maximum reliability of predicted genes.

---

## 🧠 Notes

The input DNA should be unspliced genomic sequence in our case : contig_25.fa

You can replace the Arabidopsis protein file with any annotated protein from a closely related species.

Check the version of your python with (bash $python --version), you are free to use whatever python command that aligns with your version for our provided .py program
*we use python3 as default.

You can either go step-by-step with our provided code (homologous_code.sh -> which offers a more clear scenario of each line), or run direclty the entire pipeline (homologous_pipeline.sh) -> (not recommended if you have already installed any of this on your system : Conda, Exonerate, BioPython or Bedtools, as the pipeline will direclty re-install them.)

---

## 🛠 Tools & Methods Used

This pipeline integrates a variety of established bioinformatics tools:

| Tool            | Purpose                                                |
|-----------------|--------------------------------------------------------|
| `Biopython`     | Translate DNA to protein sequences                     |
| `Exonerate`     | Protein-to-genome alignment (exon prediction)          |
| `Bedtools`      | Extract genomic coordinates and FASTA sequences        |
| `BLASTX/BLASTP` | Identify closest homologous species & proteins         |
| `T-Coffee`      | Compare predicted proteins for consistency and scoring |

---

## 🔬 Workflow Summary

1. **Translate DNA to protein** using a custom `dna2protein.py` script. To ensure the species we're working with as we'll select an homologous (specie) to compare.
2. **Run BLASTX and BLAST(protein-protein)** to determine the closest species/protein match.
3. **Use known protein** from the best match (*Arabidopsis suecica*) as a reference.
4. **Align protein to DNA** using `Exonerate` to predict exon regions.
6. **Extract exon sequences** -> CDS and re-translate to get predicted proteins, you can also compare both ab initio obtained CDS and the one obtained using this method. (important)
7. **Combine predictions** from Exonerate and ab initio tools.
8. **Compare all results** using `T-Coffee` to assess reliability.

---

## 🧪 Output
cds_comparison.fa : Combined file where we have the predicted CDS from each method. Crucial analysis in their comparison after enterin this file in T-Coffee (ab_initio: 2 proteins, 2 CDS; homology-based: 1 protein, 1 CDS - from all 6 exonic regions in all_exons.fa)

pred_proteins_exonerate.fa: Protein sequence predicted from all exon regions alignment

comparison_all.fa: Combined file with all predicted proteins (including those obtained from ab-initio gene prediction mehod -> ready for T-Coffee)

result.score_html: T-Coffee score visualization (if run)
