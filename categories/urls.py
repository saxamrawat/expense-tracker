from django.urls import path
from .views import (
    CategoryListView, CategoryCreateView,
    CategoryUpdateView, CategoryDeleteView, CategoryDetailView
)

app_name = "categories"

urlpatterns = [
    path("", CategoryListView.as_view(), name="list"),
    path("create/", CategoryCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", CategoryUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", CategoryDeleteView.as_view(), name="delete"),
    path("<int:pk>/", CategoryDetailView.as_view(), name="detail"),
]
