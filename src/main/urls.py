from django.urls import path
from . import views

urlpatterns = [
    path('fan_output', views.ServerDataView.as_view()),

]
