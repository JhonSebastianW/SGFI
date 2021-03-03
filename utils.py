from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
from xhtml2pdf import pisa
from django.http import HttpResponse
from io import BytesIO
import os
import qrcode
import shutil
def enviarCorreo(user,mail,asunto,contenido):
    context={'cont': contenido, 'mail': mail, 'user': user}
    template = get_template('correo.html')
    content = template.render(context)
    email= EmailMultiAlternatives(
        asunto,
        'SGFI',
        settings.EMAIL_HOST_USER,
        [mail]
    )
    email.attach_alternative(content,'text/html')
    email.send()
    print("Se envio.!!!!!!")

def render_to_pdf(template_src,context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), dest=response, link_callback=fetch_resources )
    if not pdf.err:
        return HttpResponse(response.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse("Error Rendering PDF", status=400)

def fetch_resources(uri, rel):
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    return path

def crearQR(cadena,nombre):
    imagen= qrcode.make(cadena)
    dir='sgfi/static/sgfi/qr/'
    nombreArchivo=nombre+".png"
    imagen.save(nombreArchivo)
    try:
        os.remove(dir+nombreArchivo)
    except:
        pass
    shutil.move(nombreArchivo,dir)
    direccion=dir+nombreArchivo
    return direccion