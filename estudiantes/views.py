import json

from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Estudiante

CAMPOS = ["nombre", "matricula", "carrera", "semestre", "correo"]


def convertir(e):
    
    return {
        "id": e.id,
        "nombre": e.nombre,
        "matricula": e.matricula,
        "carrera": e.carrera,
        "semestre": e.semestre,
        "correo": e.correo,
    }


def guardar(e, request):
    
    try:
        datos = json.loads(request.body)
        for campo in CAMPOS:
            if str(datos[campo]).strip() == "":
                return "El campo " + campo + " es obligatorio."
        e.nombre = str(datos["nombre"]).strip()
        e.matricula = str(datos["matricula"]).strip()
        e.carrera = str(datos["carrera"]).strip()
        e.semestre = int(datos["semestre"])
        e.correo = str(datos["correo"]).strip()
        e.save()
    except (ValueError, KeyError, TypeError):
        return "Datos incompletos o inválidos."
    except IntegrityError:
        return "La matrícula ya existe."
    return None



@csrf_exempt
def estudiante_lista(request):
    
    if request.method == "GET":
        estudiantes = Estudiante.objects.order_by("id")
        return JsonResponse([convertir(e) for e in estudiantes], safe=False)

   
    if request.method == "POST":
        e = Estudiante()
        error = guardar(e, request)
        if error:
            return JsonResponse({"error": error}, status=400)
        return JsonResponse(convertir(e), status=201)

    return JsonResponse({"error": "Método no permitido."}, status=405)


@csrf_exempt
def estudiante_detalle(request, pk):
    e = Estudiante.objects.filter(pk=pk).first()
    if e is None:
        return JsonResponse({"error": "Estudiante no encontrado."}, status=404)

    
    if request.method == "GET":
        return JsonResponse(convertir(e))

    
    if request.method == "PUT":
        error = guardar(e, request)
        if error:
            return JsonResponse({"error": error}, status=400)
        return JsonResponse(convertir(e))

   
    if request.method == "DELETE":
        e.delete()
        return JsonResponse({"mensaje": "Estudiante eliminado."})

    return JsonResponse({"error": "Método no permitido."}, status=405)
