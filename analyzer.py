!pip install biopython -q
print("Ready for ICIPE bioinformatics!")
from Bio import SeqIO
from io import StringIO

fasta_data = """>PF3D7_test1
ATGCAAATATATATGCAAGATATATATATATATGCAAATATATATAT
>PF3D7_test2
ATGCAAATATATATATATATGCAAGATATATATATATATGCAAATATAT
"""

def analyze():
    for record in SeqIO.parse(StringIO(fasta_data), "fasta"):
        seq = str(record.seq)
        gc = (seq.count('G') + seq.count('C')) / len(seq) * 100
        print(f"{record.id} | Length: {len(seq)} | GC%: {gc:.1f}%")

analyze()
