from django.contrib import admin

from . import models, forms
# Register your models here.


admin.site.register(models.Role)
admin.site.register(models.Profile)
admin.site.register(models.User, forms.UserAdmin)
