from django.contrib import admin
from core.models import B2CRequest
from django.contrib.admin.utils import flatten_fieldsets


@admin.register(B2CRequest)
class B2CRequestAdmin(admin.ModelAdmin):
    list_display = ('phone', 'amount')