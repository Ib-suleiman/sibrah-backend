from django.contrib import admin
from .models import PaystackTransaction


@admin.register(PaystackTransaction)
class PaystackTransactionAdmin(admin.ModelAdmin):
    list_display  = ('reference', 'email', 'amount', 'purpose',
                     'status', 'channel', 'paid_at', 'created_at')
    list_filter   = ('status', 'purpose', 'channel')
    search_fields = ('reference', 'email', 'paystack_id')
    readonly_fields = ('reference', 'paystack_id', 'amount_kobo',
                       'paid_at', 'created_at', 'updated_at')
    ordering      = ('-created_at',)

    def has_add_permission(self, request):
        return False   # Transactions are created by the system only
