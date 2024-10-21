from django.contrib import admin
from .models import CustomUser, ModelProfile
# Register your models here

admin.site.register(CustomUser)
admin.site.register(ModelProfile)