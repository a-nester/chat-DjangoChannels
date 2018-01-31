from django.urls import path
from .views import index

app_name = "my"

urlpatterns = [
    path('', index, name="index")
]