from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q, F
from django.utils import timezone
from datetime import datetime
from decimal import Decimal
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
    return redirect('accounts:login')


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


@login_required
def monthly_report(request):
    """
    Monthly summary:
    - ?month=YYYY-MM (defaults to current month)
    - total_income, total_expense, net
    - category-wise breakdown
    """
    month_param = request.GET.get("month", "").strip()
    if month_param:
        try:
            parsed = datetime.strptime(month_param, "%Y-%m")
            year = parsed.year
            month = parsed.month
            selected_month = f"{year:04d}-{month:02d}"
        except ValueError:
            today = timezone.localdate()
            year, month = today.year, today.month
            selected_month = f"{year:04d}-{month:02d}"
    else:
        today = timezone.localdate()
        year, month = today.year, today.month
        selected_month = f"{year:04d}-{month:02d}"

    # Base queryset for the user in the requested month
    qs = Transaction.objects.filter(
        user=request.user, date__year=year, date__month=month)

    # Totals
    totals = qs.aggregate(
        total_income=Sum('amount', filter=Q(type='IN')),
        total_expense=Sum('amount', filter=Q(type='EX')),
    )
    total_income = totals.get('total_income') or Decimal('0.00')
    total_expense = totals.get('total_expense') or Decimal('0.00')
    net = total_income - total_expense

    # Category-wise breakdown (use safe alias names to avoid conflicts with model fields)
    cat_qs = (
        qs
        .values(cat_id=F('category__id'), cat_name=F('category__name'))
        .annotate(
            cat_income=Sum('amount', filter=Q(type='IN')),
            cat_expense=Sum('amount', filter=Q(type='EX'))
        )
        .order_by('-cat_expense')
    )

    # Normalize None to Decimal('0.00') and compute expense share
    breakdown = []
    for row in cat_qs:
        cat_id = row.get('cat_id')
        name = row.get('cat_name') or "Uncategorized"
        c_income = row.get('cat_income') or Decimal('0.00')
        c_expense = row.get('cat_expense') or Decimal('0.00')
        if total_expense and total_expense != 0:
            share = (c_expense / total_expense) * 100
        else:
            share = Decimal('0.00')
        breakdown.append({
            "category_id": cat_id,
            "category_name": name,
            "income": c_income,
            "expense": c_expense,
            "expense_share_pct": round(share, 2),
        })

    # Month options (last 24 months) for selector
    months = []
    today = timezone.localdate()
    y = today.year
    m = today.month
    for i in range(0, 24):
        mi = m - i
        yi = y
        if mi <= 0:
            mi += 12
            yi -= 1
        key = f"{yi:04d}-{mi:02d}"
        label = f"{yi}-{mi:02d}"
        months.append((key, label))

    context = {
        "selected_month": selected_month,
        "month_options": months,
        "total_income": total_income,
        "total_expense": total_expense,
        "net": net,
        "breakdown": breakdown,
    }
    return render(request, "accounts/monthly_report.html", context)
