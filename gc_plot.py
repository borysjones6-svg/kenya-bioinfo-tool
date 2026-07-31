import matplotlib.pyplot as plt

# Simulated GC data for your malaria sequences
sequences = {
    "PF3D7_test1": 28.5,
    "PF3D7_test2": 32.1,
    "Anopheles_COI": 35.8
}

def plot_gc(data):
    names = list(data.keys())
    gc_values = list(data.values())
    
    plt.figure(figsize=(6,4))
    plt.bar(names, gc_values, color=['#2E86AB', '#A23B72', '#F18F01'])
    plt.ylabel('GC Content %')
    plt.title('GC Content of Malaria & Mosquito Sequences - Kayole Analysis')
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig('gc_plot.png')
    print("Plot saved as gc_plot.png - Upload this image to GitHub!")
    # Show values
    for k,v in data.items():
        print(f"{k}: {v}% GC")

if __name__ == "__main__":
    plot_gc(sequences)
