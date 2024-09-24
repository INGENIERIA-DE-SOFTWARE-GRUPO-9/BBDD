from django.contrib import admin
from .models import *

class MicuentaAdmin(admin.ModelAdmin):
  readonly_fields = ('created', )
  
admin.site.register(informe,MicuentaAdmin)
admin.site.register(habitacion)
