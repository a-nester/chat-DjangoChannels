from django.urls import path
from .views import log_in, log_out, sign_up


app_name = "users"
urlpatterns = [
    path('login/', log_in, name="log_in"),
    path('logout/', log_out, name="log_out"),
    path('register/', sign_up, name="register"),
]