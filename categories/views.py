# categories/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db.models import Q
from .models import Category
from .forms import CategoryForm
from transactions.models import Transaction

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "categories/category_list.html"
    context_object_name = "categories"
    paginate_by = 20

    def get_queryset(self):
        """
        Show categories that belong to the user OR global categories (user is NULL).
        Order user categories first, then global ones (optional).
        """
        qs = Category.objects.filter(Q(user=self.request.user) | Q(user__isnull=True)).order_by("-created_at")
        return qs


class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = "categories/category_detail.html"
    context_object_name = "category"

    def get_queryset(self):
        # Ensure user cannot view another user's category
        return Category.objects.filter(user=self.request.user)

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "categories/category_form.html"
    success_url = reverse_lazy("categories:list")

    def form_valid(self, form):
        # attach the current user before saving
        form.instance.user = self.request.user
        return super().form_valid(form)

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "categories/category_form.html"
    success_url = reverse_lazy("categories:list")

    def get_queryset(self):
        # limit editable objects to those owned by the request.user
        return Category.objects.filter(user=self.request.user)

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = "categories/category_confirm_delete.html"
    success_url = reverse_lazy("categories:list")

    def get_queryset(self):
        # only allow deletion of categories owned by the request.user
        return Category.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        """
        Override POST so we can check for related Transactions and refuse deletion
        with a friendly message + redirect if any exist.
        """
        self.object = self.get_object()
        # Check whether any transactions reference this category
        uses = Transaction.objects.filter(category=self.object).exists()
        if uses:
            messages.error(request, "Cannot delete this category because it is used by one or more transactions.")
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)
