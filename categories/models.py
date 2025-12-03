from django.db import models
from django.conf import settings

# Create your models here.

class Category(models.Model):
    INCOME = "IN"
    EXPENSE = "EX"
    KIND_CHOICES = [
        (INCOME, "Income"),
        (EXPENSE, "Expense"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="categories",
        null=True,
        blank=True
    )

    name = models.CharField(max_length=100)
    kind = models.CharField(max_length=2, choices=KIND_CHOICES, default=EXPENSE)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ("user", "name")
        ordering = ["-created_at"]
        verbose_name_plural = "categories"

    def __str__(self):
        return f"{self.name} ({self.get_kind_display()})"
