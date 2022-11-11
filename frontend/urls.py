from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create-page/', views.create_page),
    path('edit/<int:id>', views.edit_notes),
    path('favourite/<int:id>', views.add_favourite),
    path('delete/<int:id>', views.delete_notes),
    path('sign-up/', views.sign_up),
    path('login/', views.login_user),
    path('logout/', views.logout_user)
]
