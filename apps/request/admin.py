# Vendor
from django.contrib import admin
# Local
from .models import MemesRequest


@admin.register(MemesRequest)
class MemesRequestAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ('id', 'image', 'message', 'created_at')
    search_fields = ['message', ]
    readonly_fields = [
        'created_at',
        'updated_at',
        'deleted_at'
                       ]
