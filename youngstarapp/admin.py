from django.contrib import admin, messages
from django.db.models import Sum, Count
from django.utils.html import format_html
from .models import Contribution, LoanInquiry


@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'month', 'year', 'created_at')
    list_filter = ('month', 'year')
    search_fields = ('user__username',)

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset

            # Group by year and month and get totals
            totals = (
                qs.values('year', 'month')
                  .annotate(total_amount=Sum('amount'), count=Count('id'))
                  .order_by('-year', '-month')
            )

            # Add a message for each month
            for entry in totals:
                year = entry['year']
                month = entry['month']
                total_amount = entry['total_amount']
                count = entry['count']

                messages.info(
                    request,
                    format_html(
                        f"🧾 <strong>{month:02}/{year}</strong> — "
                        f"Total: ₦{total_amount:,.2f} from {count} contribution(s)"
                    )
                )

        except (AttributeError, KeyError):
            pass 

        return response


@admin.register(LoanInquiry)
class LoanInquiryAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'banked', 'submitted_at')
    list_filter = ('banked', 'submitted_at')
    search_fields = ('user__username', 'reason')
