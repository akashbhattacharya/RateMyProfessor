from django.contrib import admin
from .models import Professor, ModuleInstance, Module, Ratings

# Register your models here.
admin.site.register(Professor)
admin.site.register(Module)
admin.site.register(ModuleInstance)
admin.site.register(Ratings)