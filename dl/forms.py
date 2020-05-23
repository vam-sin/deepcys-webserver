from django import forms

class DLForm(forms.Form):
    pdb = forms.CharField(label='PDB ID', max_length=4, required=True)
    res = forms.IntegerField(label='Residue Number', required=True)
    chain = forms.CharField(label='Chain Letter', max_length=1, required=True)

class DLSeqForm(forms.Form):
    uniprotid = forms.CharField(label='Uniprot Accession Number', max_length=10, required=True)
    res = forms.IntegerField(label='Residue Number', required=True)
    chain = forms.CharField(label='Chain Letter', max_length=1, required=True)