from django.contrib import admin

# Register your models here.
from . import models, forms

admin.site.register(models.Role)
admin.site.register(models.Profile)
admin.site.register(models.TwoFactor)
admin.site.register(models.User, forms.UserAdmin)