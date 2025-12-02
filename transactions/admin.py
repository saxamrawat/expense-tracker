from django.contrib import admin
from .models import Transaction
# Register your models here.


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "type", "amount", "category", "date")
    list_filter = ("type", "date", "category")
    search_fields = ("description", "user__username", "category__name")
    date_hierarchy = "date"
    raw_id_fields = ("user",)
