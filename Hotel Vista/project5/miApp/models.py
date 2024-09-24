from django.db import models
from django.contrib.auth.models import User

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