

# Register your models here.
from django.contrib import admin
from .models import Contribution

@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'month', 'year', 'created_at')
    list_filter = ('month', 'year')
    search_fields = ('user__username',)
