from django.urls import path
from .views import signup_view, login_view, logout_view, monthly_report

app_name = "accounts"

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("reports/month/", monthly_report, name="monthly_report"),
]
