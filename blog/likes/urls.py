from django.urls import path
from . import views
from .api import views

urlpatterns = [
    path('', views.LikeListView.as_view(), name='list_like'),
    path('create/', views.LikeCreateView.as_view(), name='create_like'),
    path('<int:pk>/', views.LikeDetailView.as_view(), name='detail_like')
]