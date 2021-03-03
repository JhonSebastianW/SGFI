import random
from typing import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from .models import Empresa,Sede,Empleado,Tipo,Producto,Factura,ProductosFactura,Cliente
from .forms import *
from .utils import *
host='181.61.187.11'
class contactoView(View):
	succes_url = reverse_lazy('sgfi:all')
	template = 'sgfi/contacto.html'
	def get(self, request):
		return render(request,self.template)
class faqView(View):
	succes_url = reverse_lazy('sgfi:all')
	template = 'sgfi/faq.html'
	def get(self, request):
		return render(request,self.template)

class loginView(View):
	model=Empresa
	succes_url = reverse_lazy('sgfi:all')
	template = 'sgfi/login.html'
	form = EmpresaLogin()

	def get(self, request):
		if request.user.is_authenticated:
			return HttpResponseRedirect('/')
		else:
			return render(request,self.template,{'form': self.form})

	def post(self, request):
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			valuenext= request.POST.get('next')
			if(valuenext is not None):
				return HttpResponseRedirect(request.POST.get('next'))
			else:
				return HttpResponseRedirect('/login/')
		else:
			return redirect('/login/')

class recuperar(View):
	model = Empresa
	template = 'sgfi/recuperar.html'
	form = EmpresaRecuperarPwd()
	def get(self, request):
		return render(request, self.template,{'form': self.form, 'titulo': "Recuperar Cuenta"})
	def post(self, request):
		username = request.POST['username']
		email = request.POST['email']
		try:
			empresa = get_object_or_404(self.model, username=username)
			if(username==empresa.username and email==empresa.email):
				token= str(random.randrange(10))+str(random.randrange(10))+str(random.randrange(10))+str(random.randrange(10))
				empresa.token=token
				empresa.save()
				url='http://'+host+':8000/recuperar/pwd/'+empresa.username+'_'+token+'/'
				enviarCorreo(empresa.username, empresa.email, "Recuperacion de cuenta.",
						 "Hola " + empresa.username + ", haz intentado recuperar tu contraseña en SGFI. ingresa a "+url)
				return redirect('/login/')
			else:
				print("Error al intentar cambiar contraseña")
				return redirect('/recuperar/')
		except:
			return redirect('/recuperar/')

class recuperarPwd(View):
	login_url = '/login/'
	succes_url = reverse_lazy('sgfi:all')
	template = 'sgfi/recuperar.html'
	form = EmpresaEditarPwd()
	model=Empresa
	def get(self, request,token):
		try:
			inf = token.split('_')
			empresa = get_object_or_404(self.model, username=inf[0])
			if (inf[1] == empresa.token and empresa.token != ""):
				return render(request, self.template,{'form': self.form, 'titulo': "Nueva Contraseña"})
			else:
				return redirect('/login/')
		except:
			return redirect('/login/')

	def post(self, request,token):
		password = request.POST['password']
		rPassword = request.POST['rPassword']
		try:
			inf = token.split('_')
			empresa = get_object_or_404(self.model, username=inf[0])
			if (inf[1] == empresa.token and empresa.token != ""):
					if(password==rPassword):
						empresa.set_password(password)
						empresa.token=""
						empresa.save()
						enviarCorreo(empresa.username, empresa.email, "Contraseña Actualizada.",
										   empresa.username + ", tu contraseña ha sido actualizada exitosamente. ")
					return redirect('/login/')
			else:
				return redirect('/recuperar/')
		except:
			return redirect('/registro/')

class logoutView(View):
	def get(self,request):
		logout(request)
		return HttpResponseRedirect('/login/')

class mainView(LoginRequiredMixin,View):
	login_url = '/login/'
	succes_url = reverse_lazy('sgfi:all')
	def get(self,request):
		if(request.user.username=='Admin'):
			return redirect('/administrador/')
		else:
			return redirect('/empresa/')

class adminMain(LoginRequiredMixin,View):
	login_url = '/login/'
	succes_url = reverse_lazy('sgfi:all')
	template = 'sgfi/adminMain.html'
	def get(self, request):
		if (request.user.username == 'Admin'):
			return render(request, self.template)
		else:
			return redirect('/logout/')

class adminRegistrarEmpresa(LoginRequiredMixin,View):
	login_url = '/login/'
	succes_url = reverse_lazy('sgfi:all')
	template = 'sgfi/adminRegistroEmpresa.html'
	form = EmpresaRegistrar()
	def get(self, request):
		if (request.user.username == 'Admin'):
			return render(request, self.template,{'form': self.form})
		else:
			return redirect('/logout/')
	def post(self, request):
		username = request.POST['username']
		nombre = request.POST['nombre']
		email = request.POST['email']
		password = request.POST['password']
		lema = request.POST['lema']
		logo = request.FILES.get('logo')
		try:
			empresa = Empresa.objects.create_user(username=username, nombre=nombre,
												  email=email, password=password,
												  lema=lema, logo=logo,
												  estado=True)
			enviarCorreo(username, email, "Creacion de cuenta SGFI.",
						 "Hola " + username + ", haz creado una cuenta en SGFI.")
			empresa.save()
			return redirect('/administrador/empresas/')
		except:
			return redirect('administrador/empresa/registrar/')

class adminEmpresas(LoginRequiredMixin,View):
	login_url = '/login/'
	succes_url = reverse_lazy('sgfi:all')
	template = 'sgfi/adminEmpresas.html'
	def get(self, request):
		if (request.user.username == 'Admin'):
			empresas=Empresa.objects.all()
			ctx={'listaEmpresas': empresas}
			return render(request, self.template,ctx)
		else:
			return redirect('/logout/')

class adminEditarEmpresa(LoginRequiredMixin,View):
	login_url = '/login/'
	succes_url = reverse_lazy('sgfi:all')
	template = 'sgfi/adminEditarEmpresa.html'
	model=Empresa

	def get(self, request,pk):
		if (request.user.username == 'Admin'):
			empresa = get_object_or_404(self.model,pk=pk)
			form = EmpresaEditar(instance=empresa)
			ctx = {'form': form}
			return render(request, self.template, ctx)
		else:
			return redirect('/logout/')
	def post(self,request,pk):
		empresa = get_object_or_404(self.model, pk=pk)
		form = EmpresaEditar(request.POST,instance=empresa)
		if not form.is_valid():
			ctx = {'form': form}
			return render(request, self.template, ctx)
		form.save()
		return redirect('/administrador/empresas/')

class adminEditarEmpresaPwd(LoginRequiredMixin,View):
	login_url = '/login/'
	succes_url = reverse_lazy('sgfi:all')
	template = 'sgfi/empresaEditarPwd.html'
	form = EmpresaEditarPwd()
	def get(self, request,pk):
		if (request.user.username != 'Admin' and request.user.estado==True):
			return render(request, self.template,{'form': self.form})
		else:
			return redirect('/logout/')
	def post(self, request,pk):
		empresa = get_object_or_404(self.model, pk=pk)
		password = request.POST['password']
		rPassword = request.POST['rPassword']
		try:
			if(password==rPassword):
				empresa.set_password(password)
				empresa.save()
			return redirect('/empresa/')
		except:
			return redirect('/empresa/editarPwd')



class empresaMain(LoginRequiredMixin,View):
	login_url = '/login/'
	succes_url = reverse_lazy('sgfi:all')
	template = 'sgfi/empresaMain.html'
	def get(self, request):
		if (request.user.username != 'Admin' and request.user.estado==True):
			return render(request, self.template)
		else:
			return redirect('/logout/')

class empresaEditarPwd(LoginRequiredMixin,View):
	login_url = '/login/'
	succes_url = reverse_lazy('sgfi:all')
	template = 'sgfi/empresaEditarPwd.html'
	form = EmpresaEditarPwd()
	def get(self, request,token):
		if (request.user.username != 'Admin' and request.user.estado==True):
			return render(request, self.template,{'form': self.form})
		else:
			return redirect('/logout/')
	def post(self, request,token):
		password = request.POST['password']
		rPassword = request.POST['rPassword']
		if(token==request.user.token and request.user.token!=""):
			try:
				if(password==rPassword):
					request.user.set_password(password)
					request.user.save()
				return redirect('/empresa/')
			except:
				return redirect('/empresa/editarPwd')
		else:
			return redirect('/logout/')

class empresaRegistrarSede(LoginRequiredMixin,View):
	login_url = '/login/'
	succes_url = reverse_lazy('sgfi:all')
	template = 'sgfi/empresaRegistrarSede.html'
	form = SedeRegistrar()
	def get(self, request):
		if (request.user.username != 'Admin' and request.user.estado==True):
			return render(request, self.template,{'form': self.form})
		else:
			return redirect('/logout/')

	def post(self, request):
		codigo = request.POST['codigo']
		nombre = request.POST['nombre']
		direccion = request.POST['direccion']
		telefono = request.POST['telefono']
		ciudad = request.POST['ciudad']

		try:
			sede = Sede.objects.create(codigo=codigo,nombre=nombre,direccion=direccion,telefono=telefono,ciudad=ciudad,empresa=request.user)
			sede.save()
			return redirect('/empresa/sedes/')
		except:
			return redirect('/empresa/sede/registrar/')

class empresaSedes(LoginRequiredMixin,View):
	login_url = '/login/'
	succes_url = reverse_lazy('sgfi:all')
	template = 'sgfi/empresaSedes.html'
	def get(self, request):
		if (request.user.username != 'Admin' and request.user.estado==True):
			Sede.objects.all()
			sedes=Sede.objects.filter(empresa=request.user)
			ctx={'listaSedes': sedes}
			return render(request, self.template,ctx)
		else:
			return redirect('/logout/')


class empresaEditarSede(LoginRequiredMixin,View):
	login_url = '/login/'
	succes_url = reverse_lazy('sgfi:all')
	template = 'sgfi/empresaEditarSede.html'
	model=Sede

	def get(self, request,pk):
		if (request.user.username != 'Admin' and request.user.estado==True):
			sede = get_object_or_404(self.model,pk=pk)
			form = SedeEditar(instance=sede)
			ctx = {'form': form}
			return render(request, self.template, ctx)
		else:
			return redirect('/logout/')
	def post(self,request,pk):
		sede = get_object_or_404(self.model, pk=pk)
		form = SedeEditar(request.POST,instance=sede)
		if not form.is_valid():
			ctx = {'form': form}
			return render(request, self.template, ctx)
		form.save()
		return redirect('/empresa/sedes/')

class empresaRegistrarEmpleado(LoginRequiredMixin,View):
	login_url = '/login/'
	succes_url = reverse_lazy('sgfi:all')
	template = 'sgfi/empresaRegistrarEmpleado.html'
	form = EmpleadoRegistrar()

	def get(self, request):
		if (request.user.username != 'Admin' and request.user.estado==True):
			self.form.fields['sede'].queryset = Sede.objects.filter(empresa=request.user)
			return render(request, self.template,{'form': self.form})
		else:
			return redirect('/logout/')

	def post(self, request):
		username = request.POST['username']
		primerNombre = request.POST['primerNombre']
		primerApellido = request.POST['primerApellido']
		email = request.POST['email']
		password = request.POST['password']
		sede = request.POST['sede']
		rol = request.POST['rol']
		try:
			sedeObj=Sede.objects.get(codigo=str(sede))
			empleado = Empleado.objects.create(username=username,primerApellido=primerApellido,primerNombre=primerNombre,email=email,password=password,sede=sedeObj,rol=rol)
			empleado.save()
			return redirect('/empresa/empleados/')
		except:
			return redirect('/empresa/empleado/registrar/')

class empresaEmpleados(LoginRequiredMixin,View):
	login_url = '/login/'
	succes_url = reverse_lazy('sgfi:all')
	template = 'sgfi/empresaEmpleados.html'
	def get(self, request):
		if (request.user.username != 'Admin' and request.user.estado==True):
			Sede.objects.all()
			sedes=Sede.objects.filter(empresa=request.user)
			Empleado.objects.all()
			empleados=Empleado.objects.filter(sede__in=sedes)
			ctx={'listaEmpleados': empleados}
			return render(request, self.template,ctx)
		else:
			return redirect('/logout/')

class empresaEditarEmpleado(LoginRequiredMixin,View):
	login_url = '/login/'
	succes_url = reverse_lazy('sgfi:all')
	template = 'sgfi/empresaEditarEmpleado.html'
	model=Empleado
	def get(self, request,pk):
		if (request.user.username != 'Admin' and request.user.estado==True):
			empleado = get_object_or_404(self.model,pk=pk)
			form = EmpleadoEditar(instance=empleado)
			form.fields['sede'].queryset = Sede.objects.filter(empresa=request.user)
			ctx = {'form': form}
			return render(request, self.template, ctx)
		else:
			return redirect('/logout/')
	def post(self,request,pk):
		empleado = get_object_or_404(self.model, pk=pk)
		form = EmpleadoEditar(request.POST,instance=empleado)
		if not form.is_valid():
			ctx = {'form': form}
			return render(request, self.template, ctx)
		form.save()
		return redirect('/empresa/empleados/')

class empresaRegistrarTipo(LoginRequiredMixin,View):
	login_url = '/login/'
	succes_url = reverse_lazy('sgfi:all')
	template = 'sgfi/empresaRegistrarTipo.html'
	form = TipoRegistrar()
	def get(self, request):
		if (request.user.username != 'Admin' and request.user.estado==True):
			return render(request, self.template,{'form': self.form})
		else:
			return redirect('/logout/')

	def post(self, request):
		codigo = request.POST['codigo']
		descripcion = request.POST['descripcion']
		nombre = request.POST['nombre']
		try:
			tipo = Tipo.objects.create(codigo=codigo,nombre=nombre,descripcion=descripcion,empresa=request.user)
			tipo.save()
			return redirect('/empresa/productos/tipos/')
		except:
			return redirect('/empresa/productos/tipo/registrar/')

class empresaTipos(LoginRequiredMixin,View):
	login_url = '/login/'
	succes_url = reverse_lazy('sgfi:all')
	template = 'sgfi/empresaTipos.html'
	def get(self, request):
		if (request.user.username != 'Admin' and request.user.estado==True):
			Tipo.objects.all()
			tipos=Tipo.objects.filter(empresa=request.user)
			ctx={'listaTipos': tipos}
			return render(request, self.template,ctx)
		else:
			return redirect('/logout/')

class empresaEditarTipo(LoginRequiredMixin,View):
	login_url = '/login/'
	succes_url = reverse_lazy('sgfi:all')
	template = 'sgfi/empresaEditarTipo.html'
	model=Tipo
	def get(self, request,pk):
		if (request.user.username != 'Admin' and request.user.estado==True):
			tipo = get_object_or_404(self.model,codigo=pk)
			form = TipoEditar(instance=tipo)
			ctx = {'form': form}
			return render(request, self.template, ctx)
		else:
			return redirect('/logout/')
	def post(self,request,pk):
		tipo = get_object_or_404(self.model, codigo=pk)
		form = TipoEditar(request.POST,instance=tipo)
		if not form.is_valid():
			ctx = {'form': form}
			return render(request, self.template, ctx)
		form.save()
		return redirect('/empresa/productos/tipos/')


class empresaRegistrarProducto(LoginRequiredMixin,View):
	login_url = '/login/'
	succes_url = reverse_lazy('sgfi:all')
	template = 'sgfi/empresaRegistrarProducto.html'
	form = ProductoRegistrar()
	def get(self, request):
		if (request.user.username != 'Admin' and request.user.estado==True):
			self.form.fields['sede'].queryset = Sede.objects.filter(empresa=request.user)
			self.form.fields['tipo'].queryset = Tipo.objects.filter(empresa=request.user)
			return render(request, self.template,{'form': self.form})
		else:
			return redirect('/logout/')

	def post(self, request):
		referencia = request.POST['referencia']
		nombre = request.POST['nombre']
		valor = request.POST['valor']
		iva = request.POST['iva']
		stock = request.POST['stock']
		descripcion = request.POST['descripcion']
		tipo = request.POST['tipo']
		sede = request.POST['sede']
		imagen = request.FILES.get('imagen')
		try:
			sedeObj = Sede.objects.get(codigo=str(sede))
			tipoObj = Tipo.objects.get(codigo=str(tipo))
			producto = Producto.objects.create(referencia=referencia,nombre=nombre,valor=valor,iva=iva,stock=stock,descripcion=descripcion,tipo=tipoObj,sede=sedeObj,imagen=imagen)
			producto.save()
			return redirect('/empresa/productos/tipos/')
		except:
			return redirect('/empresa/productos/tipo/registrar/')

class empresaProductos(LoginRequiredMixin,View):
	login_url = '/login/'
	succes_url = reverse_lazy('sgfi:all')
	template = 'sgfi/empresaProductos.html'
	def get(self, request):
		if (request.user.username != 'Admin' and request.user.estado==True):
			sedes = Sede.objects.filter(empresa=request.user)
			productos =Producto.objects.filter(sede__in=sedes)
			ctx={'listaProductos': productos}
			return render(request, self.template,ctx)
		else:
			return redirect('/logout/')


class empresaEditarProducto(LoginRequiredMixin,View):
	login_url = '/login/'
	succes_url = reverse_lazy('sgfi:all')
	template = 'sgfi/empresaEditarProducto.html'
	model=Producto
	def get(self, request,pk):
		if (request.user.username != 'Admin' and request.user.estado==True):
			producto = get_object_or_404(self.model,referencia=pk)
			form = ProductoEditar(instance=producto)
			ctx = {'form': form}
			return render(request, self.template, ctx)
		else:
			return redirect('/logout/')
	def post(self,request,pk):
		producto = get_object_or_404(self.model, referencia=pk)
		form = ProductoEditar(request.POST,instance=producto)
		if not form.is_valid():
			ctx = {'form': form}
			return render(request, self.template, ctx)
		form.save()
		return redirect('/empresa/productos/')


class empresaRegistrarFactura(LoginRequiredMixin,View):
	login_url = '/login/'
	succes_url = reverse_lazy('sgfi:all')
	template = 'sgfi/empresaRegistrarFactura.html'
	form = FacturaRegistrar()
	def get(self, request):
		fields = ['cliente', 'empleado']
		if (request.user.username != 'Admin' and request.user.estado==True):
			Sede.objects.all()
			sedes = Sede.objects.filter(empresa=request.user)
			Empleado.objects.all()
			self.form.fields['empleado'].queryset = Empleado.objects.filter(sede__in=sedes)
			return render(request, self.template,{'form': self.form})
		else:
			return redirect('/logout/')

	def post(self, request):
		empleado = request.POST['empleado']
		cliente = request.POST['cliente']
		try:
			empleadoObj = Empleado.objects.get(id=str(empleado))
			clienteObj = Cliente.objects.get(cedula=str(cliente))
			factura = Factura.objects.create(cliente=clienteObj,empleado=empleadoObj,estado=True)
			factura.save()
			return redirect('/empresa/factura/'+str(factura.numero)+'/facturar/')
		except:
			return redirect('/empresa/factura/registrar/')

class empresaFacturas(LoginRequiredMixin,View):
	login_url = '/login/'
	succes_url = reverse_lazy('sgfi:all')
	template = 'sgfi/empresaFacturas.html'
	def get(self, request):
		if (request.user.username != 'Admin' and request.user.estado==True):
			sedes = Sede.objects.filter(empresa=request.user)
			empleados =Empleado.objects.filter(sede__in=sedes)
			facturas = Factura.objects.filter(empleado__in=empleados).order_by('numero')
			productosFactura=[]
			productos = []
			total = []
			for i in range(len(facturas)):
				productosFactura.append(ProductosFactura.objects.filter(factura=facturas[i]))
				productos.append([])
				total.append(0)
			for i in range(len(productosFactura)):
				for j in range(len(productosFactura[i])):
					productos[i].append(productosFactura[i][j].producto)
			for i in range(len(productos)):
				facturas[i].nProductos=len(productos[i])
				for j in range(len(productos[i])):
					total[i]+=productos[i][j].valor+(productos[i][j].valor*productos[i][j].iva)
			for i in range(len(facturas)):
				facturas[i].total=total[i]
			for i in range(len(facturas)):
				if(facturas[i].nProductos==0):
					facturas[i].delete()
			ctx={'listaFacturas': facturas}
			return render(request, self.template,ctx)
		else:
			return redirect('/logout/')

class empresaEditarFactura(LoginRequiredMixin,View):
	login_url = '/login/'
	succes_url = reverse_lazy('sgfi:all')
	template = 'sgfi/empresaEditarFactura.html'
	model=Factura
	def get(self, request,pk):
		if (request.user.username != 'Admin' and request.user.estado==True):
			factura = get_object_or_404(self.model,numero=pk)
			form = FacturaEditar(instance=factura)
			Sede.objects.all()
			sedes = Sede.objects.filter(empresa=request.user)
			Empleado.objects.all()
			form.fields['empleado'].queryset = Empleado.objects.filter(sede__in=sedes)
			ctx = {'form': form}
			return render(request, self.template, ctx)
		else:
			return redirect('/logout/')
	def post(self,request,pk):
		factura = get_object_or_404(self.model, numero=pk)
		form = FacturaEditar(request.POST,instance=factura)
		if not form.is_valid():
			ctx = {'form': form}
			return render(request, self.template, ctx)
		form.save()
		return redirect('/empresa/facturas/')

class empresaProductosFacturaAgregar(LoginRequiredMixin,View):
	login_url = '/login/'
	succes_url = reverse_lazy('sgfi:all')
	template = 'sgfi/empresaAgregarProducto.html'
	form = ProductosFacturaRegistrar()
	def get(self, request,pk):
		if (request.user.username != 'Admin' and request.user.estado == True):
			factura= Factura.objects.get(numero=pk)
			productosFactura=ProductosFactura.objects.filter(factura=factura)
			productos=[]
			iva=0
			total=0
			for i in range(len(productosFactura)):
				productos.append(productosFactura[i].producto)
			for i in range(len(productos)):
				iva+=productos[i].valor*productos[i].iva
				total+=productos[i].valor
			sedes = Sede.objects.filter(empresa=request.user)
			self.form.fields['producto'].queryset = Producto.objects.filter(sede__in=sedes)
			empleado = factura.empleado
			sede = empleado.sede
			ctx = {'listaProductosFactura': productos,'form': self.form,'total': total,'iva': iva, 'factura': factura,
				   'empleado': empleado, 'sede': sede}
			return render(request, self.template,ctx)
		else:
			return redirect('/logout/')

	def post(self, request,pk):
		factura= Factura.objects.get(numero=pk)
		producto = request.POST['producto']
		try:
			productoObj=Producto.objects.get(referencia=str(producto))
			productoObj.stock=productoObj.stock-1
			productoObj.save()
			productoFactura=ProductosFactura.objects.create(factura=factura,producto=productoObj)
			productoFactura.save()

			return redirect('/empresa/factura/'+str(pk)+'/facturar/')
		except:
			return redirect('/empresa/factura/'+str(pk)+'/facturar/')


class empresaProductosFacturaVer(LoginRequiredMixin,View):
	login_url = '/login/'
	succes_url = reverse_lazy('sgfi:all')
	template = 'sgfi/empresaProductosFactura.html'
	def get(self, request,pk):
		if (request.user.username != 'Admin' and request.user.estado == True):
			factura= Factura.objects.get(numero=pk)
			productosFactura=ProductosFactura.objects.filter(factura=factura)
			empleado = factura.empleado
			sede = empleado.sede
			if(sede.empresa.username==request.user.username):
				productos=[]
				iva=0
				total=0
				for i in range(len(productosFactura)):
					productos.append(productosFactura[i].producto)
				for i in range(len(productos)):
					iva+=productos[i].valor*productos[i].iva
					total+=productos[i].valor
				neto = total+iva
				direc=crearQR(host+'/empresa/factura/'+str(pk)+'/pdf/',str(pk))
				ctx = {'listaProductosFactura': productos,'total': neto,'subtotal': total,'iva': iva, 'factura': factura, 'empleado': empleado,'sede': sede, 'dirQR': direc}
				return render(request, self.template,ctx)
			else:
				return redirect('/empresa/facturas/')
		else:
			return redirect('/logout/')

class empresaProductosFacturaPdf(LoginRequiredMixin,View):
	login_url = '/login/'
	succes_url = reverse_lazy('sgfi:all')
	template = 'sgfi/factura.html'
	def get(self, request, pk):
		if (request.user.username != 'Admin' and request.user.estado == True):
			factura = Factura.objects.get(numero=pk)
			productosFactura = ProductosFactura.objects.filter(factura=factura)
			empleado = factura.empleado
			sede = empleado.sede
			if (sede.empresa.username == request.user.username):
				productos = []
				iva = 0
				total = 0
				for i in range(len(productosFactura)):
					productos.append(productosFactura[i].producto)
				for i in range(len(productos)):
					iva += productos[i].valor * productos[i].iva
					total += productos[i].valor
				neto = total+iva
				ctx = {'listaProductosFactura': productos,'total': neto,'subtotal': total,'iva': iva, 'factura': factura,
					   'empleado': empleado, 'sede': sede, 'user': request.user}
				pdf=render_to_pdf(self.template,ctx)
				return HttpResponse(pdf, content_type='application/pdf')
			else:
				return redirect('/empresa/facturas/')
		else:
			return redirect('/logout/')


class empresaInformes(LoginRequiredMixin,View):
	login_url = '/login/'
	succes_url = reverse_lazy('sgfi:all')
	template = 'sgfi/empresaInformes.html'
	def get(self, request):
		if (request.user.username != 'Admin' and request.user.estado==True):
			return render(request, self.template)
		else:
			return redirect('/logout/')

class empresaInformeEmpleados(LoginRequiredMixin,View):
	login_url = '/login/'
	succes_url = reverse_lazy('sgfi:all')
	template = 'sgfi/informeEmpleados.html'
	def get(self, request):
		if (request.user.username != 'Admin' and request.user.estado == True):
			sedes = Sede.objects.filter(empresa=request.user)
			Empleado.objects.all()
			empleados = Empleado.objects.filter(sede__in=sedes)
			ctx = {'listaEmpleados': empleados, 'titulo':"Empleados" , 'user': request.user}
			pdf=render_to_pdf(self.template,ctx)
			return HttpResponse(pdf, content_type='application/pdf')
		else:
			return redirect('/logout/')

class empresaInformeSedes(LoginRequiredMixin,View):
	login_url = '/login/'
	succes_url = reverse_lazy('sgfi:all')
	template = 'sgfi/informeSedes.html'
	def get(self, request):
		if (request.user.username != 'Admin' and request.user.estado == True):
			sedes = Sede.objects.filter(empresa=request.user)
			ctx = {'listaSedes': sedes, 'titulo':"Sedes" , 'user': request.user}
			pdf=render_to_pdf(self.template,ctx)
			return HttpResponse(pdf, content_type='application/pdf')
		else:
			return redirect('/logout/')

class empresaInformeProductos(LoginRequiredMixin,View):
	login_url = '/login/'
	succes_url = reverse_lazy('sgfi:all')
	template = 'sgfi/informeProductos.html'
	def get(self, request):
		if (request.user.username != 'Admin' and request.user.estado == True):
			sedes = Sede.objects.filter(empresa=request.user)
			productos = Producto.objects.filter(sede__in=sedes)
			ctx = {'listaProductos': productos, 'titulo':"Productos" , 'user': request.user}
			pdf=render_to_pdf(self.template,ctx)
			return HttpResponse(pdf, content_type='application/pdf')
		else:
			return redirect('/logout/')

class empresaInformeVentas(LoginRequiredMixin,View):
	login_url = '/login/'
	succes_url = reverse_lazy('sgfi:all')
	template = 'sgfi/informeFacturas.html'
	def get(self, request):
		if (request.user.username != 'Admin' and request.user.estado == True):
			sedes = Sede.objects.filter(empresa=request.user)
			empleados = Empleado.objects.filter(sede__in=sedes)
			facturas = Factura.objects.filter(empleado__in=empleados).order_by('numero')
			productosFactura = []
			productos = []
			total = []
			for i in range(len(facturas)):
				productosFactura.append(ProductosFactura.objects.filter(factura=facturas[i]))
				productos.append([])
				total.append(0)
			for i in range(len(productosFactura)):
				for j in range(len(productosFactura[i])):
					productos[i].append(productosFactura[i][j].producto)
			for i in range(len(productos)):
				facturas[i].nProductos = len(productos[i])
				for j in range(len(productos[i])):
					total[i] += productos[i][j].valor + (productos[i][j].valor * productos[i][j].iva)
			for i in range(len(facturas)):
				facturas[i].total = total[i]
			for i in range(len(facturas)):
				if (facturas[i].nProductos == 0):
					facturas[i].delete()
			ctx = {'listaFacturas': facturas, 'titulo':"Ventas" , 'user': request.user}
			pdf=render_to_pdf(self.template,ctx)
			return HttpResponse(pdf, content_type='application/pdf')
		else:
			return redirect('/logout/')

class empresaEnviarCorreo(LoginRequiredMixin,View):
	login_url = '/login/'
	succes_url = reverse_lazy('sgfi:all')
	template = 'sgfi/empresaEnviarCorreo.html'
	form = EnviarEmail()
	def get(self, request):
		if (request.user.username != 'Admin' and request.user.estado==True):
			return render(request, self.template,{'form': self.form})
		else:
			return redirect('/logout/')
	def post(self, request):
		opcion = request.POST['opcion']
		mensaje = request.POST['mensaje']
		try:
			if(opcion=='empleados'):
				sedes = Sede.objects.filter(empresa=request.user)
				Empleado.objects.all()
				empleados = Empleado.objects.filter(sede__in=sedes)
				for i in range(len(empleados)):
					enviarCorreo(empleados[i].primerNombre,empleados[i].email,"Correo Masivo", mensaje)
			else:
				sedes = Sede.objects.filter(empresa=request.user)
				empleados = Empleado.objects.filter(sede__in=sedes)
				facturas = Factura.objects.filter(empleado__in=empleados).values('cliente').distinct()
				clientes = Cliente.objects.filter(cedula__in=facturas)
				for i in range(len(clientes)):
					enviarCorreo(clientes[i].nombre,clientes[i].email,"Correo Masivo", mensaje)
			return redirect('/empresa/correo/')
		except:
			return redirect('/empresa/')

class registroEmpresa(View):
	login_url = '/login/'
	succes_url = reverse_lazy('sgfi:all')
	template = 'sgfi/recuperar.html'
	form = EmpresaRegistrar()
	def get(self, request):
		return render(request, self.template, {'form': self.form})

	def post(self, request):
		username = request.POST['username']
		nombre = request.POST['nombre']
		email = request.POST['email']
		password = request.POST['password']
		lema = request.POST['lema']
		logo = request.FILES.get('logo')
		try:
			empresa = Empresa.objects.create_user(username=username, nombre=nombre,
												  email=email, password=password,
												  lema=lema, logo=logo,
												  estado=True)
			enviarCorreo(username, email, "Creacion de cuenta SGFI.",
						 "Hola " + username + ", haz creado una cuenta en SGFI.")
			empresa.save()
			return redirect('/login/')
		except:
			return redirect('/login/')

