from django.contrib import admin
from .models import Log, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	pass

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
	pass
