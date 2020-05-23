from django.http import HttpResponse, HttpResponseRedirect
from .forms import DLForm, DLSeqForm
from django.shortcuts import render
from .keras_app import app_backend

# Figure out how to send classes variable to the other file 
# With that done, you will have very less things left to do. OMG MOOD.

def predict_struct(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = DLForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            pdb = request.POST.get('pdb')
            res = request.POST.get('res')
            chain = request.POST.get('chain')
            print(pdb, res, chain)
            classes, prediction, pred_max = app_backend.predict_class(pdb, res, chain)
            one = prediction[0]
            two = prediction[1]
            three = prediction[2]
            four = prediction[3]
            class_one = classes[0]
            class_two = classes[1]
            class_three = classes[2]
            class_four = classes[3]

            return render(request, 'results.html', {'one': one, 'two': two, 'three': three, 'four': four, 'pred_max': pred_max, 'class_one': class_one, 'class_two': class_two, 'class_three': class_three, 'class_four': class_four})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = DLForm()

    return render(request, 'predict_struct.html', {'form': form})


def predict_seq(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = DLSeqForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            uniprotid = request.POST.get('uniprotid')
            uniprotid = uniprotid.replace(' ', '')
            res = request.POST.get('res')
            chain = request.POST.get('chain')
            print(uniprotid, res, chain)
            classes, prediction, pred_max = app_backend.predict_seq_class(uniprotid, res, chain)
            one = prediction[0]
            two = prediction[1]
            three = prediction[2]
            four = prediction[3]
            class_one = classes[0]
            class_two = classes[1]
            class_three = classes[2]
            class_four = classes[3]

            return render(request, 'results.html', {'one': one, 'two': two, 'three': three, 'four': four, 'pred_max': pred_max, 'class_one': class_one, 'class_two': class_two, 'class_three': class_three, 'class_four': class_four})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = DLSeqForm()

    return render(request, 'predict_seq.html', {'form': form})

def results(request):
    return render(request, 'results.html')


