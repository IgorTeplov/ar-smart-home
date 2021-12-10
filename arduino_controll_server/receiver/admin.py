from django.contrib import admin
from .models import CommandLog, EnterLog 

@admin.register(CommandLog)
class CommandLogAdmin(admin.ModelAdmin):
	pass

@admin.register(EnterLog)
class EnterLogAdmin(admin.ModelAdmin):
	pass
