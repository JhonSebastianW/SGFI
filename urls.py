from django.urls import path

from . import views
app_name = 'sgfi'
urlpatterns = [
    path('', views.mainView.as_view(), name='main'),

    path('faq/', views.faqView.as_view(), name='faq'),
    path('contacto/', views.contactoView.as_view(), name='contacto'),

    path('login/', views.loginView.as_view(), name='login'),
    path('logout/', views.logoutView.as_view(), name='logout'),
    path('recuperar/', views.recuperar.as_view(), name='recuperar'),
    path('recuperar/pwd/<str:token>/', views.recuperarPwd.as_view(), name='recuperarPwd'),

    path('administrador/', views.adminMain.as_view(), name='adminMain'),
    path('administrador/empresa/registrar/', views.adminRegistrarEmpresa.as_view(), name='adminRegistrarEmpresa'),
    path('administrador/empresas/', views.adminEmpresas.as_view(), name='adminEmpresas'),
    path('administrador/empresa/<int:pk>/editar/', views.adminEditarEmpresa.as_view(), name='adminEditarEmpresa'),

    path('empresa/', views.empresaMain.as_view(), name='empresaMain'),
    path('empresa/editar/pwd/<str:token>', views.empresaEditarPwd.as_view(), name='empresaEditarPwd'),
    path('empresa/sede/registrar/', views.empresaRegistrarSede.as_view(), name='empresaRegistrarSede'),
    path('empresa/sedes/', views.empresaSedes.as_view(), name='empresaSedes'),
    path('empresa/sede/<str:pk>/editar', views.empresaEditarSede.as_view(), name='empresaEditarSede'),


    path('empresa/empleado/registrar/', views.empresaRegistrarEmpleado.as_view(), name='empresaRegistrarEmpleado'),
    path('empresa/empleados/', views.empresaEmpleados.as_view(), name='empresaEmpleados'),
    path('empresa/empleado/<int:pk>/editar/', views.empresaEditarEmpleado.as_view(), name='empresaEditarEmpleado'),

    path('empresa/productos/tipo/registrar/', views.empresaRegistrarTipo.as_view(), name='empresaRegistrarTipo'),
    path('empresa/productos/tipos/', views.empresaTipos.as_view(), name='empresaTipos'),
    path('empresa/productos/tipo/<str:pk>/editar/', views.empresaEditarTipo.as_view(), name='empresaEditarTipo'),

    path('empresa/producto/registrar/', views.empresaRegistrarProducto.as_view(), name='empresaRegistrarProducto'),
    path('empresa/productos/', views.empresaProductos.as_view(), name='empresaProductos'),
    path('empresa/producto/<str:pk>/editar/', views.empresaEditarProducto.as_view(), name='empresaEditarProducto'),

    path('empresa/factura/registrar/', views.empresaRegistrarFactura.as_view(), name='empresaRegistrarFactura'),
    path('empresa/facturas/', views.empresaFacturas.as_view(), name='empresaFacturas'),
    path('empresa/factura/<int:pk>/editar/', views.empresaEditarFactura.as_view(), name='empresaEditarFactura'),

    path('empresa/factura/<int:pk>/facturar/', views.empresaProductosFacturaAgregar.as_view(), name='empresaProductosFactura'),
    path('empresa/factura/<int:pk>/ver/', views.empresaProductosFacturaVer.as_view(), name='empresaProductosFacturaVer'),
    path('empresa/factura/<int:pk>/pdf/', views.empresaProductosFacturaPdf.as_view(), name='empresaProductosFacturaPdf'),

    path('empresa/informes/', views.empresaInformes.as_view(), name='empresaInformes'),
    path('empresa/informe/sedes/', views.empresaInformeSedes.as_view(), name='empresaInformeSedesPdf'),
    path('empresa/informe/empleados/', views.empresaInformeEmpleados.as_view(), name='empresaInformeEmpleadosPdf'),
    path('empresa/informe/productos/', views.empresaInformeProductos.as_view(), name='empresaInformeProductosPdf'),
    path('empresa/informe/ventas/', views.empresaInformeVentas.as_view(), name='empresaInformeVentasPdf'),

    path('empresa/correo/', views.empresaEnviarCorreo.as_view(), name='empresaEnviarCorreo'),

    path('registro/', views.registroEmpresa.as_view(), name='registro'),



]