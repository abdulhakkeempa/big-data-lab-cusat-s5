import sys

word_counts = {}

for line in sys.stdin:
    line = line.strip()
    if ' ' in line:
        word, count = line.strip().split(' ', 1)
        try:
            count = int(count)
        except ValueError:
            continue
        if word in word_counts:
            word_counts[word] += count
        else:
            word_counts[word] = count

# Print the word counts
for word, count in word_counts.items():
    print('%s\t%s' % (word, count))
