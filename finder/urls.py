from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_view, name='search_view'),
    path('search-form/', views.search_form, name='search_form'),
]
