from django.urls import path

from . import views

urlpatterns = [
  path('', views.index),
  path('register', views.register),
  path('login', views.login),
  path('logout', views.logout),
  path('dashboard', views.dashboard),
  path('password/new', views.new),
  path('password/create_password', views.create_password),
  path('password/remove/<int:id>', views.remove_password),
  path('password/edit_password/<int:id>', views.update_password),
  path('password/edit/<int:id>', views.edit_password),
  path('password/<int:id>', views.show_password),
]