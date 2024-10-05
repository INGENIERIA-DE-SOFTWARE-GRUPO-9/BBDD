from django.contrib import admin
from .models import informe, habitacion, reserva

class MicuentaAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)  # Añadir el CSS personalizado
        }

admin.site.site_header = "Hotel  Vista Administración"  # Cambia el título en la cabecera del panel
admin.site.site_title = "Hotel  Vista Administración"  # Cambia el título del navegador
admin.site.index_title = "Bienvenido a la Administración"

admin.site.register(informe, MicuentaAdmin)
admin.site.register(habitacion)
admin.site.register(reserva)
