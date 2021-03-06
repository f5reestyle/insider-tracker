from django.contrib import admin
from .models import File,Firm,SIC,Stock,Insider
# Register your models here.
@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    pass
@admin.register(Firm)
class FirmAdmin(admin.ModelAdmin):
    search_fields = ['cik','ticker','sic']
@admin.register(SIC)
class SICAdmin(admin.ModelAdmin):
    pass
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    search_fields=['ticker']