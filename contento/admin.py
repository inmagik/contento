from django.contrib import admin
from .models import Page

admin.site.register(Page)

class PageAdmin(admin.ModelAdmin):
    readonly_fields = ['fullpath']
