from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from .forms import UserSignupForm
from transactions.models import Transaction
from decimal import Decimal

# Create your views here.


def signup_view(request):
    if request.method == "POST":
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login
            return redirect("dashboard")
    else:
        form = UserSignupForm()

    return render(request, "accounts/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):

    # conditional aggregration
    totals = (
        Transaction.objects.filter(user=request.user).aggregate(
            total_income=Sum("amount", filter=Q(type="IN")),
            total_expense=Sum("amount", filter=Q(type="EX")),
        )
    )

    # avoiding none results from SUM by defaulting to decimal (0.0)

    total_income = totals.get("total_income") or Decimal("0.00")
    total_expense = totals.get("total_expense") or Decimal("0.00")
    net_savings = total_income - total_expense

    # Last 5 transactions(newest first)

    recent_transactions = (
        Transaction.objects.filter(
            user=request.user).order_by("-date", "-id")[:5]
    )

    context = {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_savings": net_savings,
        "recent_transactions": recent_transactions,
    }

    return render(request, "dashboard.html", context)
