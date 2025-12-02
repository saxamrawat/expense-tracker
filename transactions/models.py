from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
from categories.models import Category


class Transaction(models.Model):

    amount = models.DecimalField(
        max_digits=12, decimal_places=2, help_text="Amount in your currency")

    INCOME = "IN"
    EXPENSE = "EX"
    TRANSACTION_TYPE_CHOICES = [
        (INCOME, "Income"),
        (EXPENSE, "Expense"),
    ]
    type = models.CharField(
        max_length=2, choices=TRANSACTION_TYPE_CHOICES, default=EXPENSE)

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="transactions")

    description = models.TextField(blank=True)

    date = models.DateField(default=timezone.now)

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    class Meta:
        ordering = ["-date", "-id"]

    def __str__(self):
        return f"{self.get_type_display()}: {self.amount} - {self.category.name if self.category.name else "No Category"} ({self.date})"
