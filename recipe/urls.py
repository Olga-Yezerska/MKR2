from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('category/<int:pk>/', views.category_detail, name='category_detail'),
]