# Input: PDB, Residue ID, Chain
# Output: Class

# Libraries
# from schrodinger.protein.getpdb import download_fasta, get_pdb
# import tensorflow.compat.v1 as tf
# tf.disable_v2_behavior()
import requests 
import numpy as np
from tensorflow.keras.models import load_model
import pickle
from urllib.request import urlopen
import os
from .feature_gen import get_nf1, get_nf2, get_nf3, get_nf4, get_nf5, get_seq_nf5
from .pka_website import get_pka
from .Bf_rhpy_website import get_bf_rhpy
import keras.backend.tensorflow_backend as tb
tb._SYMBOLIC_SCOPE.value = True

# Take in PDB ID and residue ID. (Ex: 1b2l, 137, A, Output: Disulfide)

def predict_class(pdb, res, chain):
	# Parameters:
	res = int(res)

	# print(pdb, res)

	# Calculate pKa, rHpy, BF, Str (Need to Scale them also)

	# Get FASTA and PDB.
	PROJECT_PATH = os.path.dirname(__file__) + "/"
	print(PROJECT_PATH)
	print("\nSteps.")
	url = 'https://files.rcsb.org/download/' + pdb.upper() + '.pdb'
	r = requests.get(url)
	filename_pdb = PROJECT_PATH + '/PDB_Data/' + pdb + '.pdb'
	open(filename_pdb, 'wb').write(r.content)
	print("Obtained PDB.")

	url = 'https://www.rcsb.org/pdb/download/downloadFile.do?fileFormat=fastachain&compression=NO&structureId=' + pdb.lower() + '&chainId=' + chain
	r = requests.get(url)
	filename_fasta = PROJECT_PATH + '/PDB_fasta/' + pdb + '.fasta'
	open(filename_fasta, 'wb').write(r.content)
	print("Obtained fasta.")

	# pKa 
	pKa = get_pka(pdb, res, chain)
	# pKa = 11.23
	print("pKa Calculation Done: " + str(pKa))

	# BF_RHPY
	BF, rHpy = get_bf_rhpy(pdb, res, chain)
	print("Calculated BF and rHpy: " + str(BF) + ", " + str(rHpy))

	# NF1 (Works)
	nf1_13 = get_nf1(pdb, res, chain, 13)

	print("Calculated NF1.")
	# print("NF1 " + str(nf1))

	# NF2 (Works)
	nf2_8, nf2_7, nf2_6, nf2_5 = get_nf2(pdb, res, chain)

	print("Calculated NF2.")
	# print("NF2: " + str(nf2))

	# NF3
	nf3 = get_nf3(pdb)
	print(nf3)
	print("Calculated NF3")
	
	# NF4
	nf4_3 = get_nf4(pdb, res, chain, 3)
	nf4_5 = get_nf4(pdb, res, chain, 5)
	nf4_7 = get_nf4(pdb, res, chain, 7)
	nf4_9 = get_nf4(pdb, res, chain, 9)
	nf4_11 = get_nf4(pdb, res, chain, 11)
	nf4_13 = get_nf4(pdb, res, chain, 13)

	print("Calculated NF4")
	# NF5 (Works)
	nf5_13 = get_nf5(pdb, res, chain, 13)

	# print("Calculated NF5.")
	# print("NF5 " + str(nf5))

	# Compile X
	X = []
	X.append(pKa)
	X.append(BF)
	X.append(rHpy)

	for i in nf1_13:
		X.append(i)

	for i in nf2_5:
		X.append(i)
	for i in nf2_6:
		X.append(i)
	for i in nf2_7:
		X.append(i)
	for i in nf2_8:
		X.append(i)

	for i in nf3:
		X.append(i)

	for i in nf4_3:
		X.append(i)
	for i in nf4_5:
		X.append(i)
	for i in nf4_7:
		X.append(i)
	for i in nf4_9:
		X.append(i)
	for i in nf4_11:
		X.append(i)
	for i in nf4_13:
		X.append(i)

	for i in nf5_13:
		X.append(i)

	X = np.asarray(X)
	X = np.reshape(X, (len(X),))
	X = np.array([X,])
	X = np.expand_dims(X, axis=2)
	# print(X.shape)
	# # Load Model and Predict
	model_path = PROJECT_PATH + '/cnn_ann.h5'
	classifier = load_model(model_path)
	# classifier = load_model('/home/banshee/Academics/Sem6/BioFormal/Website/cystein_webserver/dl/keras_app/ann.h5')
	prediction = classifier.predict(X)
	prediction = prediction[0]
	prediction = list(prediction)
	for i in range(len(prediction)):
		prediction[i] *= 100 
		prediction[i] = float("{:.2f}".format(prediction[i]))
	# Print Results
	classes = ['Disulphide', 'Sulphenylation', 'Metal-Binding', 'Thioether']
	print("\nProbaility Results:-")
	print("Disulphide: " + str(prediction[0]) + '%')
	print("Selphenylation: " + str(prediction[1]) + '%')
	print("Metal-Binding: " + str(prediction[2]) + '%')
	print("Thioether: " + str(prediction[3]) + '%')
	print("\n")
	pred_max = prediction.index(max(prediction))
	print("Highest Probability to be " + classes[pred_max]) 

	print("Structure Prediction")

	return classes, prediction, pred_max

def predict_seq_class(uniprotid, res, chain):
	# Parameters:
	res = int(res)

	# print(pdb, res)

	# Calculate pKa, rHpy, BF, Str (Need to Scale them also)

	# Get FASTA and PDB.
	PROJECT_PATH = os.path.dirname(__file__) + "/"
	print(PROJECT_PATH)
	print("\nSteps.")


	uid = uniprotid.upper()

	filename_fasta = PROJECT_PATH + '/PDB_fasta/' + uid + '.fasta'

	cmd = 'efetch -db protein -format fasta -id ' + uid 
	
	a = os.popen(cmd).read()
	a = a.split('\n')
	seq = ''
	for i in range(1, len(a)):
		seq += a[i]

	print("Obtained FASTA")
	
	# NF5 (Works)
	nf5_13 = get_seq_nf5(seq, res, chain, 13) 

	# print("Calculated NF5.")
	# print("NF5 " + str(nf5))

	# Compile X
	X = []

	for i in nf5_13:
		X.append(i)

	X = np.asarray(X)
	dim1 = len(X)
	dim2 = 13*2 + 1

	X = X.reshape(1, dim2, 1)
	X = X.astype(np.float32)
	# print(X.shape)
	# # Load Model and Predict
	model_path = PROJECT_PATH + '/gru.h5'
	classifier = load_model(model_path)
	# classifier = load_model('/home/banshee/Academics/Sem6/BioFormal/Website/cystein_webserver/dl/keras_app/ann.h5')
	prediction = classifier.predict(X)
	print(prediction)
	prediction = prediction[0]
	prediction = list(prediction)
	for i in range(len(prediction)):
		prediction[i] *= 100 
		prediction[i] = float("{:.2f}".format(prediction[i]))
	# Print Results
	classes = ['Disulphide', 'Sulphenylation', 'Metal-Binding', 'Thioether']
	print("\nProbaility Results:-")
	print("Disulphide: " + str(prediction[0]) + '%')
	print("Selphenylation: " + str(prediction[1]) + '%')
	print("Metal-Binding: " + str(prediction[2]) + '%')
	print("Thioether: " + str(prediction[3]) + '%')
	print("\n")
	pred_max = prediction.index(max(prediction))
	print("Highest Probability to be " + classes[pred_max]) 
	print("Sequence Prediction")

	return classes, prediction, pred_max

if __name__ == '__main__':
	pdb = input("Enter PDB ID: ").upper()
	res = int(input("Enter Residue ID: "))
	chain = input("Enter Chain Alphabet: ").upper()

	predict_seq_class(pdb, res, chain)


