import sys, csv
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

ds = SupervisedDataSet(20, 1)

misspellings = []

def convert(string):
  final = []
  for i in xrange(len(string)):
    final.append("{0:03d}".format(ord(string[i])))
  while len(final) < 20:
    final.append("000")
  final = map(int, final)
  return final
 
def unconvert(number):
  final = ""
 
  for chunk in number:
    if int(chunk) < 0:
      chunk = 0
    final += chr(int(chunk))
 
  final = final.replace(chr(0), "")
  return final

def tests():
	if "conner" == unconvert(convert("conner")):
		print "Passed the plain text test."
	else: 
		sys.exit("Error! Convert function didn't pass the plain text test!")

	if "con-ner" == unconvert(convert("con-ner")):
		print "Passed the dash test."
	else:
		sys.exit("Error! Convert function didn't pass the dash test!")

	if "con ner" == unconvert(convert("con ner")):
		print "Passed the space test."
	else: 
		sys.exit("Error! Convert function didn't pass the space test!")

	if "CONNER" == unconvert(convert("CONNER")):
		print "Passed the capital test."
	else: 
		sys.exit("Error! Convert function didn't pass the capital test!")

	if "conner's" == unconvert(convert("conner's")):
		print "Passed the apostrophe test."
	else: 
		sys.exit("Error! Convert function didn't pass apostrophe test!")

	if 20 == len(convert("conner")):
		print "Passed the length test. (Convert outputs are 20 characters long.)"
	else:
		sys.exit("Error! Convert function isn't returning number that are 20 characters long!")

	print "Convert is returning:",type(convert("conner")).__name__

	print convert("Conner")
tests()


def load():
	print "Loading dataset..."
	for i in xrange(10):
		with open('misspellings.csv', 'rb') as f:
			reader = csv.reader(f)
			for row in reader:
				misspellings.append(row)

		with open('data.csv', 'rb') as f:
			reader = csv.reader(f)
			for row in reader:
				misspellings.append(row)
	print len(misspellings), "items in dataset."
	print "Load of dataset finished."

load()

for i in xrange(len(misspellings)):
	print 'Adding to dataset',i,'of',len(misspellings)-1
	ds.addSample((misspellings[i][0]),(misspellings[i][1]))
	

net = buildNetwork(20, 500, 1)
trainer = BackpropTrainer(net, ds)
trainer.train()
print net.activate(convert("basicly"))