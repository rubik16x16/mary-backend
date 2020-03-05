from django.urls import path
from . import views

urlpatterns = [
  path('', views.UserAccountsList.as_view()),
  path('<int:pk>/', views.UserAccountsDetail.as_view())
]