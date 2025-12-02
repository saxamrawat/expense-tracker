from django.urls import path
from .views import TransactionCreateView, TransactionListView

app_name = "transactions"

urlpatterns = [
    path("add/",  TransactionCreateView.as_view(), name="add"),
    path("",  TransactionListView.as_view(), name="list"),
]