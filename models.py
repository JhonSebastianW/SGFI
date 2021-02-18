from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Empresa(AbstractUser):
	username = models.CharField(max_length=30, unique=True)
	nombre= models.CharField(max_length=60)
	email = models.CharField(max_length=254)
	password = models.CharField(max_length=128)
	lema = models.CharField(max_length=128)
	logo = models.ImageField(upload_to="empresas",null=True)
	estado= models.BooleanField()
	token = models.CharField(max_length=8)
	def __str__(self):
		return self.username

class Sede(models.Model):
	codigo = models.CharField(primary_key=True,max_length=30)
	nombre= models.CharField(max_length=30)
	ciudad = models.CharField(max_length=30)
	direccion= models.CharField(max_length=60)
	telefono = models.IntegerField()
	empresa = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
	def __str__(self):
		return self.codigo

class Empleado(models.Model):
	username = models.CharField(max_length=30, unique=True)
	primerNombre= models.CharField(max_length=20)
	primerApellido= models.CharField(max_length=20)
	rol = models.IntegerField()
	email = models.CharField(max_length=254)
	password = models.CharField(max_length=128)
	fechaCreado = models.DateTimeField(auto_now_add=True)
	sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
	def __str__(self):
		return self.primerNombre+" "+self.primerApellido

class Tipo(models.Model):
	codigo =  models.CharField(primary_key=True,max_length=30)
	nombre= models.CharField(max_length=30)
	descripcion = models.CharField(max_length=128)
	empresa = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
	)
	def __str__(self):
		return self.codigo


class Producto(models.Model):
	referencia =  models.CharField(primary_key=True,max_length=30)
	nombre = models.CharField(max_length=70)
	valor =  models.FloatField()
	iva =  models.FloatField()
	stock = models.IntegerField()
	descripcion = models.CharField(max_length=128)
	imagen = models.ImageField(upload_to="productos",null=True)
	sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
	tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)
	def __str__(self):
		return self.referencia

class Cliente (models.Model):
	cedula = models.IntegerField(primary_key=True)
	nombre = models.CharField(max_length=30)
	apellido = models.CharField(max_length=30)
	def __str__(self):
		return self.nombre+" "+self.apellido
	
class Factura(models.Model):
	total=0
	nProductos=0
	numero = models.AutoField(primary_key=True)
	cliente =  models.ForeignKey(Cliente, on_delete=models.CASCADE)
	estado  = models.BooleanField()
	fecha  = models.DateTimeField(auto_now_add=True)
	empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
	def __str__(self):
		return str(self.numero)


class ProductosFactura(models.Model):
	factura  = models.ForeignKey(Factura, on_delete=models.CASCADE)
	producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

