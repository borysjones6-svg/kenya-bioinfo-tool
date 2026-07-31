from Bio import SeqIO
from io import StringIO

# Sample data - replace with your malaria.fasta later in VS Code
fasta_data = """>PF3D7_test1
ATGCAAATATATATGCAAGATATATATATATATGCAAATATATATATATGTTTTTT
>Anopheles_gambiae_COI
ATGCGTTATATATATGCAAGATATATATATATATGCAAATATATATATATGAAAAA
"""

def find_motifs(fasta_text, motifs=["ATG", "TATA", "GC"]):
    print("=== Motif Finder - Gene Prediction Tool ===\n")
    for record in SeqIO.parse(StringIO(fasta_text), "fasta"):
        seq = str(record.seq).upper()
        print(f"Sequence: {record.id} | Length: {len(seq)}")
        for motif in motifs:
            count = seq.count(motif)
            positions = [i for i in range(len(seq)) if seq.startswith(motif, i)]
            print(f"  {motif}: found {count} times at positions {positions[:5]}")
        print("-" * 40)

if __name__ == "__main__":
    find_motifs(fasta_data)
