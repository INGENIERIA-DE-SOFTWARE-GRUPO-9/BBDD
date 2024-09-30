from django.db import models
from django.contrib.auth.models import User
from jsonschema import ValidationError

# Create your models here.
# PRIMERA TABLA DADA POR DJANGO COMO TABLA USUARIO, DESCRITOS PARAMETROS EN FORMS.PY


class habitacion(models.Model):
    codigo = models.CharField(max_length=4,primary_key=True)
    detalle = models.CharField(max_length=600)
    precio = models.IntegerField()
    fechadisponibilidad = models.DateField()
    oferta = models.BooleanField()
    imagen = models.CharField(max_length=600)
    tipo = models.IntegerField(default=1)

    def __str__(self):
        return self.detalle +" ("+ self.codigo +")"

class informe(models.Model):  # tabla creada para usuario admin TF pueda crear informes, se divisa en index como historial versiones
  title = models.CharField(max_length=200)
  description = models.TextField(max_length=1000)
  created = models.DateTimeField(auto_now_add=True)
  datecompleted = models.DateTimeField(null=True, blank=True)
  important = models.BooleanField(default=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.title + ' - ' + self.user.username    
  
class reserva(models.Model):
    habitacion = models.ForeignKey('habitacion', on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def clean(self):
        # Validación opcional para asegurar que fecha_fin > fecha_inicio
        if self.fecha_fin <= self.fecha_inicio:
            raise ValidationError('La fecha de fin debe ser posterior a la fecha de inicio.')

    def __str__(self):
        return f"Reserva de {self.habitacion} del {self.fecha_inicio} al {self.fecha_fin}"