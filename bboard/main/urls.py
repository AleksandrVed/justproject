from django.urls import path
from . import views
from .views import other_page

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:page>/', other_page, name='other'),
]