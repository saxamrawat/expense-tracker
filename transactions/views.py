from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import datetime
from .models import Transaction
from .forms import TransactionForm

# Create your views here.


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "transactions/add_transaction.html"
    success_url = reverse_lazy("transactions:add")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "transactions/transaction_list.html"
    context_object_name = "transactions"
    paginate_by = 20

    def get_queryset(self):
        """
        Return transactions for the logged-in user, sorted by date desc then id desc.
        If a valid 'month' GET parameter is provided in YYYY-MM format, filter by that month.
        """
        qs = Transaction.objects.filter(user=self.request.user)

        # Try to parse ?month=YYYY-MM (safe parsing, ignore invalid formats)
        month_param = self.request.GET.get("month", "").strip()
        if month_param:
            try:
                # Accept formats: "YYYY-MM" or "YYYY-M" just in case
                parsed = datetime.strptime(month_param, "%Y-%m")
                year = parsed.year
                month = parsed.month
                qs = qs.filter(date__year=year, date__month=month)
            except ValueError:
                # If parsing fails, do nothing (return unfiltered qs)
                # Optionally, you can log this if you have logging configured
                pass

        # Sort newest first, id desc as tie-breaker
        qs = qs.order_by("-date", "-id")
        return qs

    def get_context_data(self, **kwargs):
        """
        Provide month_options (last 12 months) and the selected_month for the template.
        """
        ctx = super().get_context_data(**kwargs)

        today = timezone.localdate()
        year = today.year
        month = today.month

        months = []
        for i in range(0, 12):
            m = month - i
            y = year
            if m <= 0:
                m += 12
                y -= 1
            key = f"{y:04d}-{m:02d}"  # e.g., "2025-12"
            # formatted label could be made prettier (e.g., "Dec 2025"), keep simple now
            label = f"{y}-{m:02d}"
            months.append((key, label))

        ctx["month_options"] = months
        ctx["selected_month"] = self.request.GET.get("month", "")
        return ctx


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = "transactions/transaction_confirm_delete.html"
    context_object_name = "transaction"
    success_url = reverse_lazy("transactions:list")

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
