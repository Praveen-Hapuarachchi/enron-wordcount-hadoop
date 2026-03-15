import matplotlib.pyplot as plt

# Load data from the exported file
words = []
counts = []

with open('top_words.txt', 'r') as f:
    for line in f:
        parts = line.split()
        if len(parts) == 2:
            words.append(parts[0])
            counts.append(int(parts[1]))

# Create the Bar Chart
plt.figure(figsize=(12, 7))
bars = plt.bar(words, counts, color='skyblue', edgecolor='navy')

# Add titles and labels
plt.title('Top 10 Most Frequent Words in Enron Dataset', fontsize=16, fontweight='bold')
plt.xlabel('Words', fontsize=12)
plt.ylabel('Frequency (Millions)', fontsize=12)
plt.xticks(rotation=45)

# Add data labels on top of each bar
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 50000, 
             f'{yval:,}', ha='center', va='bottom', fontsize=10)

plt.tight_layout()

# Save the plot for your report
plt.savefig('enron_wordcount_chart.png')
print("Chart saved as 'enron_wordcount_chart.png'")

# If you have a GUI/Display enabled, you can show it
plt.show()