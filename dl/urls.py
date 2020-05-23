from django.urls import path

from . import views

urlpatterns = [
    path('structure', views.predict_struct, name='predict_struct'),
    path('sequence', views.predict_seq, name='predict_seq'),
    path('results', views.results, name='results'),
]