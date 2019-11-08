from django.urls import path
from . import views

urlpatterns = [
  path('', views.TransaccionesList.as_view()),
  path('<int:id>', views.TransaccionesDetail.as_view())
]
