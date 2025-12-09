from django.urls import path
from .views import TransactionCreateView, TransactionListView, TransactionDeleteView, export_transactions_csv

app_name = "transactions"

urlpatterns = [
    path("add/",  TransactionCreateView.as_view(), name="add"),
    path("",  TransactionListView.as_view(), name="list"),
    path("<int:pk>/delete/", TransactionDeleteView.as_view(), name="delete"),
    path("export/csv/", export_transactions_csv, name="export_csv"),
]