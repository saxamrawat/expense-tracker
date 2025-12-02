from django.urls import path
from .views import TransactionCreateView, TransactionListView, TransactionDeleteView

app_name = "transactions"

urlpatterns = [
    path("add/",  TransactionCreateView.as_view(), name="add"),
    path("",  TransactionListView.as_view(), name="list"),
    path("<int:pk>/delete/", TransactionDeleteView.as_view(), name="delete")
]