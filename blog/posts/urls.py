from django.urls import path
from . import views
from .api import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='list'),
    path('create/', views.PostCreateView.as_view(), name='create_post'),
    path('<str:slug>/', views.PostDetailView.as_view(), name='detail')
]