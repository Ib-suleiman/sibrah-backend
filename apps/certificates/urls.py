from django.urls import path
from . import views

app_name = 'certificates'

urlpatterns = [
    path('verify/',         views.verify,              name='verify'),
    path('<str:code>/',     views.certificate_detail,  name='detail'),
]
