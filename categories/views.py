# categories/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Category
from .forms import CategoryForm

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "categories/category_list.html"
    context_object_name = "categories"
    paginate_by = 20

    def get_queryset(self):
        # Only return categories that belong to the logged-in user
        return Category.objects.filter(user=self.request.user).order_by("-created_at")

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
