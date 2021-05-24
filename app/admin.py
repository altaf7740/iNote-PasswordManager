from django.contrib import admin
from .models import Registration, Credential

class RegistrationAdmin(admin.ModelAdmin):
    list_display = "firstname", "lastname", "email", "password"

class CredentialAdmin(admin.ModelAdmin):
    list_display = "username", "website", "password", "userid"

# Register your models here.
admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Credential, CredentialAdmin)