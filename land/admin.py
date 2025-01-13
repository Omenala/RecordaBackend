from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Land

@admin.register(Land)
class LandAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'size', 'price', 'status', 'created_by', 'created_at')
    list_filter = ('status', 'location', 'created_at')
    search_fields = ('title', 'location', 'created_by__username')
    readonly_fields = ('created_at', 'created_by')
    fieldsets = (
        (None, {
            'fields': ('title', 'location', 'size', 'price', 'status', 'created_by', 'created_at')
        }),
    )

    def save_model(self, request, obj, form, change):
        """Ensure the logged-in user is automatically set as the creator for new entries."""
        if not obj.pk:  # If it's a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
