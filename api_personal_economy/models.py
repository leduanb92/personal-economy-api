from django.db import models
from django.utils import timezone


# Create your models here.
class Cuenta(models.Model):
    nombre = models.CharField(max_length=100)
    owner = models.ForeignKey('auth.User', related_name='cuentas', on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        """
        Capitalize the name before saving
        """
        self.nombre = self.nombre.capitalize()
        super(Cuenta, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        # unique_together = ['nombre', 'owner']


class Operacion(models.Model):
    INGRESO = 'In'
    GASTO = 'Ga'
    TIPO_CHOICES = [
        (INGRESO, 'Ingreso'),
        (GASTO, 'Gasto'),
    ]
    tipo = models.CharField(
        max_length=2,
        choices=TIPO_CHOICES,
        default=GASTO,
    )
    cuenta = models.ForeignKey(Cuenta, models.PROTECT, related_name='operaciones')
    fecha = models.DateField(default=timezone.now)
    monto = models.PositiveIntegerField()
    descripcion = models.CharField(max_length=250, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '%s de $%d a la cuenta %s el %s' %(self.get_tipo_display(), self.monto, self.cuenta.nombre, self.fecha)

    class Meta:
        ordering = ["-fecha"]
