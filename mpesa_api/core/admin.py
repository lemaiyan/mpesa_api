from django.contrib import admin

from mpesa_api.core.models import B2CRequest


@admin.register(B2CRequest)
class B2CRequestAdmin(admin.ModelAdmin):
    list_display = ('phone', 'amount')