from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.photo_list, name='photo_list'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('upload/', views.photo_upload, name='photo_upload'),
    path('delete/<int:pk>/', views.photo_delete, name='photo_delete'),
]