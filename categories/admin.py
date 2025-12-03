from django.contrib import admin
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "kind", "user", "created_at", "is_global")
    list_filter = ("kind", "created_at")
    search_fields = ("name",)

    def is_global(self, obj):
        return obj.user is None
    is_global.boolean = True
    is_global.short_description = "Global?"
