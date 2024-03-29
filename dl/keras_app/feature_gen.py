import os
from Bio.PDB.DSSP import dssp_dict_from_pdb_file
import numpy as np
from Bio.PDB import *
from Bio.PDB import PDBParser
from Bio import SeqIO
import pickle
from sklearn.preprocessing import LabelEncoder
import re

def get_nf1(pdb, res, chain, nf1_window):
	PROJECT_PATH = os.path.dirname(__file__) + "/"
	filename_pdb = PROJECT_PATH + '/PDB_Data/' + pdb + '.pdb'
	dssp = dssp_dict_from_pdb_file(filename_pdb)
	dssp = dssp[0]
	nf1 = []
	start = res - nf1_window
	end = res + nf1_window
	structure = ''
	for k, v in dssp:
		chain = k
		break
	for j in range(start-1, end):
		try:
			structure = dssp[chain, (' ', j, ' ')][1]
			if structure == 'H' or structure == 'G' or structure == 'I':
				nf1.append(1)
			elif structure == 'T' or structure == 'S':
				nf1.append(2)
			elif structure == 'B':
				nf1.append(3)
			elif structure == 'E':
				nf1.append(4)
			else:
				nf1.append(5)
		except:
			nf1.append(6)

	print("NF1_" + str(nf1_window) + ": " + str(nf1))

	return nf1

def get_nf2(pdb, res, chain):
	nf2_8_single = np.zeros(22, dtype = int)
	nf2_7_single = np.zeros(22, dtype = int)
	nf2_6_single = np.zeros(22, dtype = int)
	nf2_5_single = np.zeros(22, dtype = int) 
	PROJECT_PATH = os.path.dirname(__file__) + "/"
	filename_pdb = PROJECT_PATH + '/PDB_Data/' + pdb + '.pdb'
	parser = PDBParser()
	structure = parser.get_structure('PHA-L', filename_pdb)
	model = structure[0]
	try:
		# print(chain_[i])
		# for x in model:
		# 	print(x)
		# Iterate for all chains
		for chain in model:
			residue1 = chain[res] 
			for residue2 in chain:
				if residue1 != residue2:
					try:
						distance = residue1['CA'] - residue2['CA']
					except KeyError:
						continue
					if distance < 5: 
						# print(residue1.get_resname(), residue2.get_resname(), distance)
						if residue2.get_resname() == 'ALA':
							nf2_5_single[0] += 1
						elif residue2.get_resname() == 'ARG':
							nf2_5_single[1] += 1
						elif residue2.get_resname() == 'ASN':
							nf2_5_single[2] += 1
						elif residue2.get_resname() == 'ASP':
							nf2_5_single[3] += 1
						elif residue2.get_resname() == 'ASX':
							nf2_5_single[4] += 1
						elif residue2.get_resname() == 'CYS':
							nf2_5_single[5] += 1
						elif residue2.get_resname() == 'GLU':
							nf2_5_single[6] += 1
						elif residue2.get_resname() == 'GLN':
							nf2_5_single[7] += 1
						elif residue2.get_resname() == 'GLX':
							nf2_5_single[8] += 1
						elif residue2.get_resname() == 'GLY':
							nf2_5_single[9] += 1
						elif residue2.get_resname() == 'HIS':
							nf2_5_single[10] += 1
						elif residue2.get_resname() == 'ILE':
							nf2_5_single[11] += 1
						elif residue2.get_resname() == 'LEU':
							nf2_5_single[12] += 1
						elif residue2.get_resname() == 'LYS':
							nf2_5_single[13] += 1
						elif residue2.get_resname() == 'MET':
							nf2_5_single[14] += 1
						elif residue2.get_resname() == 'PHE':
							nf2_5_single[15] += 1
						elif residue2.get_resname() == 'PRO':
							nf2_5_single[16] += 1
						elif residue2.get_resname() == 'SER':
							nf2_5_single[17] += 1
						elif residue2.get_resname() == 'THR':
							nf2_5_single[18] += 1
						elif residue2.get_resname() == 'TRP':
							nf2_5_single[19] += 1
						elif residue2.get_resname() == 'TYR':
							nf2_5_single[20] += 1
						elif residue2.get_resname() == 'VAL':
							nf2_5_single[21] += 1
					if distance < 6:
						# print(residue1.get_resname(), residue2.get_resname(), distance)
						if residue2.get_resname() == 'ALA':
							nf2_6_single[0] += 1
						elif residue2.get_resname() == 'ARG':
							nf2_6_single[1] += 1
						elif residue2.get_resname() == 'ASN':
							nf2_6_single[2] += 1
						elif residue2.get_resname() == 'ASP':
							nf2_6_single[3] += 1
						elif residue2.get_resname() == 'ASX':
							nf2_6_single[4] += 1
						elif residue2.get_resname() == 'CYS':
							nf2_6_single[5] += 1
						elif residue2.get_resname() == 'GLU':
							nf2_6_single[6] += 1
						elif residue2.get_resname() == 'GLN':
							nf2_6_single[7] += 1
						elif residue2.get_resname() == 'GLX':
							nf2_6_single[8] += 1
						elif residue2.get_resname() == 'GLY':
							nf2_6_single[9] += 1
						elif residue2.get_resname() == 'HIS':
							nf2_6_single[10] += 1
						elif residue2.get_resname() == 'ILE':
							nf2_6_single[11] += 1
						elif residue2.get_resname() == 'LEU':
							nf2_6_single[12] += 1
						elif residue2.get_resname() == 'LYS':
							nf2_6_single[13] += 1
						elif residue2.get_resname() == 'MET':
							nf2_6_single[14] += 1
						elif residue2.get_resname() == 'PHE':
							nf2_6_single[15] += 1
						elif residue2.get_resname() == 'PRO':
							nf2_6_single[16] += 1
						elif residue2.get_resname() == 'SER':
							nf2_6_single[17] += 1
						elif residue2.get_resname() == 'THR':
							nf2_6_single[18] += 1
						elif residue2.get_resname() == 'TRP':
							nf2_6_single[19] += 1
						elif residue2.get_resname() == 'TYR':
							nf2_6_single[20] += 1
						elif residue2.get_resname() == 'VAL':
							nf2_6_single[21] += 1
					if distance < 7:
						# print(residue1.get_resname(), residue2.get_resname(), distance)
						if residue2.get_resname() == 'ALA':
							nf2_7_single[0] += 1
						elif residue2.get_resname() == 'ARG':
							nf2_7_single[1] += 1
						elif residue2.get_resname() == 'ASN':
							nf2_7_single[2] += 1
						elif residue2.get_resname() == 'ASP':
							nf2_7_single[3] += 1
						elif residue2.get_resname() == 'ASX':
							nf2_7_single[4] += 1
						elif residue2.get_resname() == 'CYS':
							nf2_7_single[5] += 1
						elif residue2.get_resname() == 'GLU':
							nf2_7_single[6] += 1
						elif residue2.get_resname() == 'GLN':
							nf2_7_single[7] += 1
						elif residue2.get_resname() == 'GLX':
							nf2_7_single[8] += 1
						elif residue2.get_resname() == 'GLY':
							nf2_7_single[9] += 1
						elif residue2.get_resname() == 'HIS':
							nf2_7_single[10] += 1
						elif residue2.get_resname() == 'ILE':
							nf2_7_single[11] += 1
						elif residue2.get_resname() == 'LEU':
							nf2_7_single[12] += 1
						elif residue2.get_resname() == 'LYS':
							nf2_7_single[13] += 1
						elif residue2.get_resname() == 'MET':
							nf2_7_single[14] += 1
						elif residue2.get_resname() == 'PHE':
							nf2_7_single[15] += 1
						elif residue2.get_resname() == 'PRO':
							nf2_7_single[16] += 1
						elif residue2.get_resname() == 'SER':
							nf2_7_single[17] += 1
						elif residue2.get_resname() == 'THR':
							nf2_7_single[18] += 1
						elif residue2.get_resname() == 'TRP':
							nf2_7_single[19] += 1
						elif residue2.get_resname() == 'TYR':
							nf2_7_single[20] += 1
						elif residue2.get_resname() == 'VAL':
							nf2_7_single[21] += 1
					if distance < 8:
						# print(residue1.get_resname(), residue2.get_resname(), distance)
						if residue2.get_resname() == 'ALA':
							nf2_8_single[0] += 1
						elif residue2.get_resname() == 'ARG':
							nf2_8_single[1] += 1
						elif residue2.get_resname() == 'ASN':
							nf2_8_single[2] += 1
						elif residue2.get_resname() == 'ASP':
							nf2_8_single[3] += 1
						elif residue2.get_resname() == 'ASX':
							nf2_8_single[4] += 1
						elif residue2.get_resname() == 'CYS':
							nf2_8_single[5] += 1
						elif residue2.get_resname() == 'GLU':
							nf2_8_single[6] += 1
						elif residue2.get_resname() == 'GLN':
							nf2_8_single[7] += 1
						elif residue2.get_resname() == 'GLX':
							nf2_8_single[8] += 1
						elif residue2.get_resname() == 'GLY':
							nf2_8_single[9] += 1
						elif residue2.get_resname() == 'HIS':
							nf2_8_single[10] += 1
						elif residue2.get_resname() == 'ILE':
							nf2_8_single[11] += 1
						elif residue2.get_resname() == 'LEU':
							nf2_8_single[12] += 1
						elif residue2.get_resname() == 'LYS':
							nf2_8_single[13] += 1
						elif residue2.get_resname() == 'MET':
							nf2_8_single[14] += 1
						elif residue2.get_resname() == 'PHE':
							nf2_8_single[15] += 1
						elif residue2.get_resname() == 'PRO':
							nf2_8_single[16] += 1
						elif residue2.get_resname() == 'SER':
							nf2_8_single[17] += 1
						elif residue2.get_resname() == 'THR':
							nf2_8_single[18] += 1
						elif residue2.get_resname() == 'TRP':
							nf2_8_single[19] += 1
						elif residue2.get_resname() == 'TYR':
							nf2_8_single[20] += 1
						elif residue2.get_resname() == 'VAL':
							nf2_8_single[21] += 1

		print(nf2_5_single)
		print(nf2_6_single)
		print(nf2_7_single)
		print(nf2_8_single)
	except:
		print("NF2 Production Failed")

	return nf2_8_single, nf2_7_single, nf2_6_single, nf2_5_single

def get_nf3(pdb):

	PROJECT_PATH = os.path.dirname(__file__) + "/"
	path_ = PROJECT_PATH + '/PDB_Data/' + pdb + '.pdb'
	infile_path = PROJECT_PATH + '/NF3_funcs.pickle'
	infile = open(infile_path,'rb')
	func = pickle.load(infile)
	infile.close()

	le = LabelEncoder()
	func = le.fit(func)
	f = open(path_, "r")

	for x in f:
		x = x.replace("HEADER    ", "")
		x = x.split(' ')
		ind_func = ''
		for j in range(5):
			ind_func += x[j]
			# ind_func += ' '
		print(ind_func)
		nf3 = le.transform([ind_func])

		break
	
	return nf3 

def get_nf4(pdb, res, chain, window):
	sing_motif = np.zeros(8)
	string = ''
	list_ind = 0
	PROJECT_PATH = os.path.dirname(__file__) + "/"
	file = PROJECT_PATH + '/PDB_fasta/' + pdb + '.fasta'

	record = list(SeqIO.parse(file, "fasta"))
	for j in range(len(record)):
		if type(chain) == str:	
			ind = record[j].id[5]
			if ind == chain:
				list_ind = j
				break
		else:
			list_ind = chain - 1

	seq = record[list_ind].seq
	start = res - window
	end = res + window
	for j in range(start-1, end):
		try:
			string += seq[j]
		except:
			string += '-'
	
	if len(re.findall(r"CC", string)) > 0:
		sing_motif[0] = 1.0
	if len(re.findall(r"C[A-Z]C", string)) > 0:
		sing_motif[1] = 1.0
	if len(re.findall(r"C[A-Z][A-Z][A-Z][A-Z]C", string)) > 0:
		sing_motif[2] = 1.0
	if len(re.findall(r"C[A-Z][A-Z][A-Z]C", string)) > 0:
		sing_motif[3] = 1.0
	if len(re.findall(r"C[A-Z][A-Z]C", string)) > 0:
		sing_motif[4] = 1.0
	if len(re.findall(r"C[A-Z][A-Z]C[A-Z][A-Z][A-Z][A-Z][A-Z]C", string)) > 0:
		sing_motif[5] = 1.0
	if len(re.findall(r"C[A-Z][A-Z]C[A-Z][A-Z]C", string)) > 0:
		sing_motif[6] = 1.0
	if len(re.findall(r"C[A-Z][A-Z]C[A-Z][A-Z]C[A-Z][A-Z][A-Z]C", string)) > 0:
		sing_motif[7] = 1.0

	print("NF4_" + str(window) + ": " + str(sing_motif))
	
	return sing_motif

def get_nf5(pdb, res, chain, nf5_window):
	PROJECT_PATH = os.path.dirname(__file__) + "/"
	filename_fasta = PROJECT_PATH + '/PDB_fasta/' + pdb + '.fasta'
	record = list(SeqIO.parse(filename_fasta, "fasta"))
	seq = record[0].seq
	start = res - nf5_window
	end = res + nf5_window
	nf5 = []
	for j in range(start-1, end):
		try:
			if seq[j] == 'A':
				nf5.append(1)
			elif seq[j] == 'R':
				nf5.append(2)
			elif seq[j] == 'N':
				nf5.append(3)
			elif seq[j] == 'D':
				nf5.append(4)
			elif seq[j] == 'B':
				nf5.append(5)
			elif seq[j] == 'C':
				nf5.append(6)
			elif seq[j] == 'E':
				nf5.append(7)
			elif seq[j] == 'Q':
				nf5.append(8)
			elif seq[j] == 'Z':
				nf5.append(9)
			elif seq[j] == 'G':
				nf5.append(10)
			elif seq[j] == 'H':
				nf5.append(11)
			elif seq[j] == 'I':
				nf5.append(12)
			elif seq[j] == 'L':
				nf5.append(13)
			elif seq[j] == 'K':
				nf5.append(14)
			elif seq[j] == 'M':
				nf5.append(15)
			elif seq[j] == 'F':
				nf5.append(16)
			elif seq[j] == 'P':
				nf5.append(17)
			elif seq[j] == 'S':
				nf5.append(18)
			elif seq[j] == 'T':
				nf5.append(19)
			elif seq[j] == 'W':
				nf5.append(20)
			elif seq[j] == 'I':
				nf5.append(21)
			elif seq[j] == 'P':
				nf5.append(22)
			else:
				nf5.append(23)
		except:
			nf5.append(24)

	print(nf5)

	return nf5

def get_seq_nf5(seq, res, chain, nf5_window):
	PROJECT_PATH = os.path.dirname(__file__) + "/"
	start = res - nf5_window
	end = res + nf5_window
	nf5 = []
	for j in range(start-1, end):
		try:
			if seq[j] == 'A':
				nf5.append(1)
			elif seq[j] == 'R':
				nf5.append(2)
			elif seq[j] == 'N':
				nf5.append(3)
			elif seq[j] == 'D':
				nf5.append(4)
			elif seq[j] == 'B':
				nf5.append(5)
			elif seq[j] == 'C':
				nf5.append(6)
			elif seq[j] == 'E':
				nf5.append(7)
			elif seq[j] == 'Q':
				nf5.append(8)
			elif seq[j] == 'Z':
				nf5.append(9)
			elif seq[j] == 'G':
				nf5.append(10)
			elif seq[j] == 'H':
				nf5.append(11)
			elif seq[j] == 'I':
				nf5.append(12)
			elif seq[j] == 'L':
				nf5.append(13)
			elif seq[j] == 'K':
				nf5.append(14)
			elif seq[j] == 'M':
				nf5.append(15)
			elif seq[j] == 'F':
				nf5.append(16)
			elif seq[j] == 'P':
				nf5.append(17)
			elif seq[j] == 'S':
				nf5.append(18)
			elif seq[j] == 'T':
				nf5.append(19)
			elif seq[j] == 'W':
				nf5.append(20)
			elif seq[j] == 'I':
				nf5.append(21)
			elif seq[j] == 'P':
				nf5.append(22)
			else:
				nf5.append(23)
		except:
			nf5.append(24)

	print(nf5)

	return nf5

