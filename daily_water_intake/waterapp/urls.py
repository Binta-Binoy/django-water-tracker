from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.intake_list, name='intake_list'),
    path('add/', views.intake_create, name='intake_create'),
    path('edit/<int:pk>/', views.intake_update, name='intake_update'),
    path('delete/<int:pk>/', views.intake_delete, name='intake_delete'),
    path('difference/', views.intake_difference, name='intake_difference'),
]
