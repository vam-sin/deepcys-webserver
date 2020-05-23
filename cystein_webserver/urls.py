from django.contrib import admin
from django.urls import include, path
from .views import index

urlpatterns = [
    path('dl/', include('dl.urls')),
    path('admin/', admin.site.urls),
    path('', index, name='index'),
]