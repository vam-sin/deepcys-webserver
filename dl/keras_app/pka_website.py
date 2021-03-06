import propka.lib, propka.molecular_container
import os
from pathlib import Path

def get_pka(pdb, residid, chain):
	try:
		PROJECT_PATH = os.path.dirname(__file__) + "/"
		options, _ = propka.lib.loadOptions()
		pdbfile = PROJECT_PATH + 'PDB_Data/' + pdb + '.pdb'
		cur_path = os.path.dirname(__file__)
		filename = os.path.join(Path(__file__).parent.parent.parent, pdb + '.pka')
		print(options, pdbfile)

		my_molecule = propka.molecular_container.Molecular_container(pdbfile, options)
		my_molecule.calculate_pka()
		my_molecule.write_pka()
		print(filename)
		print(cur_path)
		pka_val_file = open(filename, "r")
		search_results = []
		for x in pka_val_file:
			search_text1 = 'CYS'
			search_text2 = str(residid)
			search_text3 = str(chain)
			if (search_text1 in x) and (search_text2 in x) and (search_text3 in x):
				search_results.append(x)
		req_text = search_results[len(search_results)-1] 
		req_text = req_text.split(' ')
		values_req_text = []
		for j in req_text:
			if j != "":
				values_req_text.append(j)
		print(float(values_req_text[3]))
		pka_val = float(values_req_text[3])
	except:
		print("Propka Error!")
		pka_val = 0.0

	return pka_val