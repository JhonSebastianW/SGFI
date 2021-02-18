from django.forms import ModelForm
from django import forms
from sgfi.models import Empresa,Sede,Empleado,Producto,Tipo,Factura,ProductosFactura
from django.contrib.auth.forms import AuthenticationForm

class EmpresaLogin(ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = Empresa
		fields = ['username', 'password']

	def __init__(self, *args, **kwargs):
		super(EmpresaLogin, self).__init__(*args, **kwargs)
		self.fields['username'].label = "Usuario"
		self.fields['password'].label = "Contraseña"


class EmpresaRegistrar(ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = Empresa
		fields = ['username','nombre','email','password','lema','logo']
	def __init__(self, *args, **kwargs):
		super(EmpresaRegistrar, self).__init__(*args, **kwargs)
		self.fields['username'].label = "Usuario Empresa"
		self.fields['nombre'].label = "Nombre Empresa"
		self.fields['password'].label = "Contraseña"
		self.fields['email'].label = "Correo"
		self.fields['lema'].label = "Lema"
		self.fields['logo'].label = "Logo"

class EmpresaRecuperarPwd(ModelForm):
	class Meta:
		model = Empresa
		fields = ['username', 'email']
	def __init__(self, *args, **kwargs):
		super(EmpresaRecuperarPwd, self).__init__(*args, **kwargs)
		self.fields['username'].label = "Usuario"
		self.fields['email'].label = "Correo"


class EmpresaEditarPwd(ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	rPassword = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = Empresa
		fields = ['password']
	def __init__(self, *args, **kwargs):
		super(EmpresaEditarPwd, self).__init__(*args, **kwargs)
		self.fields['password'].label = "Contraseña"
		self.fields['rPassword'].label = "Repetir Contraseña"


class EmpresaEditar(ModelForm):
	class Meta:
		model = Empresa
		fields = ['nombre','lema','logo','estado']
	def __init__(self, *args, **kwargs):
		super(EmpresaEditar, self).__init__(*args, **kwargs)
		self.fields['nombre'].label = "Nombre Empresa"
		self.fields['lema'].label = "Lema"
		self.fields['logo'].label = "Logo"
		self.fields['estado'].label = "Estado"

class SedeRegistrar(ModelForm):
	class Meta:
		model=Sede
		fields=['codigo','nombre','direccion','telefono','ciudad']
	def __init__(self, *args, **kwargs):
		super(SedeRegistrar, self).__init__(*args, **kwargs)
		self.fields['codigo'].label = "Codigo"
		self.fields['nombre'].label = "Nombre"
		self.fields['direccion'].label = "Direccion"
		self.fields['telefono'].label = "Telefono"
		self.fields['ciudad'].label = "Ciudad"



class SedeEditar(ModelForm):
	class Meta:
		model=Sede
		fields=['nombre','direccion','telefono','ciudad']
	def __init__(self, *args, **kwargs):
		super(SedeEditar, self).__init__(*args, **kwargs)
		self.fields['nombre'].label = "Nombre"
		self.fields['direccion'].label = "Direccion"
		self.fields['telefono'].label = "Telefono"
		self.fields['ciudad'].label = "Ciudad"



class EmpleadoRegistrar(ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model=Empleado
		fields=['username','primerNombre','primerApellido','email','password','sede','rol']
	def __init__(self, *args, **kwargs,):
		super(EmpleadoRegistrar, self).__init__(*args, **kwargs)
		self.fields['username'].label = "Cedula"
		self.fields['primerNombre'].label = "Primer Nombre"
		self.fields['primerApellido'].label = "Primer Apellido"
		self.fields['email'].label = "Correo"
		self.fields['password'].label = "Contraseña"
		self.fields['sede'].label = "Sede"
		self.fields['rol'].label = "Rol"

class EmpleadoEditar(ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model=Empleado
		fields=['primerNombre','primerApellido','email','sede','rol']
	def __init__(self, *args, **kwargs):
		super(EmpleadoEditar, self).__init__(*args, **kwargs)
		self.fields['primerNombre'].label = "Primer Nombre"
		self.fields['primerApellido'].label = "Primer Apellido"
		self.fields['email'].label = "Correo"
		self.fields['sede'].label = "Sede"
		self.fields['rol'].label = "Rol"

class TipoRegistrar(ModelForm):
	class Meta:
		model=Tipo
		fields=['codigo','nombre','descripcion']
	def __init__(self, *args, **kwargs):
		super(TipoRegistrar, self).__init__(*args, **kwargs)
		self.fields['codigo'].label = "Codigo"
		self.fields['nombre'].label = "Nombre"
		self.fields['descripcion'].label = "Drescripcion"

class TipoEditar(ModelForm):
	class Meta:
		model=Tipo
		fields=['nombre','descripcion']
	def __init__(self, *args, **kwargs):
		super(TipoEditar, self).__init__(*args, **kwargs)
		self.fields['nombre'].label = "Nombre"
		self.fields['descripcion'].label = "Drescripcion"


class ProductoRegistrar(ModelForm):
	class Meta:
		model=Producto
		fields=['referencia','nombre','valor','iva','stock','descripcion','tipo','sede','imagen']
	def __init__(self, *args, **kwargs):
		super(ProductoRegistrar, self).__init__(*args, **kwargs)
		self.fields['referencia'].label = "Referencia"
		self.fields['nombre'].label = "Nombre"
		self.fields['valor'].label = "Valor"
		self.fields['iva'].label = "IVA"
		self.fields['stock'].label = "Stock"
		self.fields['descripcion'].label = "Descripcion"
		self.fields['tipo'].label = "Tipo"
		self.fields['sede'].label = "Sede"
		self.fields['imagen'].label = "Imagen"

class ProductoEditar(ModelForm):
	class Meta:
		model=Producto
		fields=['referencia','valor','iva','stock','imagen', 'tipo']
	def __init__(self, *args, **kwargs):
		super(ProductoEditar, self).__init__(*args, **kwargs)
		self.fields['referencia'].label = "Referencia"
		self.fields['valor'].label = "Valor"
		self.fields['iva'].label = "IVA"
		self.fields['stock'].label = "Stock"
		self.fields['tipo'].label = "Tipo"
		self.fields['imagen'].label = "Imagen"

class FacturaRegistrar(ModelForm):
	class Meta:
		model=Factura
		fields=['cliente','empleado']
	def __init__(self, *args, **kwargs):
		super(FacturaRegistrar, self).__init__(*args, **kwargs)
		self.fields['cliente'].label = "Cliente"
		self.fields['empleado'].label = "Empleado"

class FacturaEditar(ModelForm):
	class Meta:
		model=Factura
		fields=['cliente','empleado','estado']
	def __init__(self, *args, **kwargs):
		super(FacturaEditar, self).__init__(*args, **kwargs)
		self.fields['cliente'].label = "Cliente"
		self.fields['empleado'].label = "Empleado"
		self.fields['estado'].label = "Estado"


class ProductosFacturaRegistrar(ModelForm):
	class Meta:
		model=ProductosFactura
		fields=['producto']
	def __init__(self, *args, **kwargs):
		super(ProductosFacturaRegistrar, self).__init__(*args, **kwargs)
		self.fields['producto'].label = "Producto"


class EmpresaAuthForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        pass
