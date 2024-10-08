"Program Admin Models"

from django.contrib import admin
from .models import Program, Module


class ProgramAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
    )

    ordering = ('sku',)


admin.site.register(Program, ProgramAdmin)
admin.site.register(Module)
