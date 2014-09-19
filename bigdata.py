import random
letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
def mutate(word):
	mutated = random.randint(0, len(word) - 1)
	mutation = random.choice(letters)
	return word[:mutated] + mutation + word[mutated + 1:]


new_rows = []

import csv
with open('data/words.csv', 'rbU') as f:
	reader = csv.reader(f)
	for row in reader:
		for i in xrange(10):
			new_rows.append([mutate(row[0]), row[0]])

with open('data/bigdata.csv', 'wb') as f:
	writer = csv.writer(f)
	writer.writerows(new_rows)