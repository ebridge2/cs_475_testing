#!/usr/bin/python

import sys
from math import log

if len(sys.argv) != 3:
    print 'usage: %s data predictions' % sys.argv[0]
    sys.exit()

data_file = sys.argv[1]
predictions_file = sys.argv[2]

data = open(data_file)
predictions = open(predictions_file)

# Load the real labels.
true_labels = []
for line in data:
    true_labels.append(line.split()[0])

predicted_labels = []
for line in predictions:
    predicted_labels.append(line.strip())

data.close()
predictions.close()

if len(predicted_labels) != len(true_labels):
    print 'Number of lines in two files do not match.'
    sys.exit()

total = len(true_labels)

countA = {}
countB = {}
countAB = {}

for l in range(0, total):
	a = true_labels[l]
	b = predicted_labels[l]

	if a not in countA: countA[a] = 0
	if b not in countB: countB[b] = 0

	if a not in countAB: countAB[a] = {}
	if b not in countAB[a]: countAB[a][b] = 0

	countA[a] += 1
	countB[b] += 1
	countAB[a][b] += 1

pA = {}
pB = {}

HA = 0
for a in countA:
	pA[a] = float(countA[a]) / float(total)
	if pA[a] > 0: HA -= pA[a] * log(pA[a])

HB = 0
for b in countB:
	pB[b] = float(countB[b]) / float(total)
	if pB[b] > 0: HB -= pB[b] * log(pB[b])

MI = 0
for a in countA:
	for b in countB:
		if b not in countAB[a]: countAB[a][b] = 0
		pAB = float(countAB[a][b]) / float(total)

		if pAB > 0: MI += pAB * log(pAB / (pA[a]*pB[b]))

VI = HA + HB - 2.0*MI

#print "H(A)", HA
#print "H(B)", HB
#print "MI", MI

print 'VI: %f' % VI
