import datetime
import json
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Persona, Proyectos, Eventos
from .serializers import (
    EventosSerializer, 
    PersonaSerializer, 
    ProyectosSerializer,
    HorasProyectoSerializer,
    HorasPersonaSerializer,
    EstadisticasAreasSerializer,
    TipoTrabajoSerializer,
    )



# Create your views here.
class PersonasList(APIView):
    def get(self, request):
        serializer_context = {
            'request': request,
        }
        personas = Persona.objects.all()
        serializer = PersonaSerializer(personas, many=True, context=serializer_context)
        return Response(serializer.data)

class OnePerson(APIView):
    def get(self, request, id):
        serializer_context = {
            'request': request,
        }   
        personas = Persona.objects.get(pk=id)
        serializer = PersonaSerializer(personas, many=False, context=serializer_context)
        return Response(serializer.data)

class ProyectosList(APIView):
    def get(self, request):
        serializer_context = {
            'request': request,
        }
        proyectos = Proyectos.objects.all()
        serializer = ProyectosSerializer(proyectos, many=True, context=serializer_context)
        return Response(serializer.data)

class OneProject(APIView):
    def get(self, request, id):
        serializer_context = {
            'request': request,
        }
        proyectos = Proyectos.objects.get(pk=id)
        serializer = ProyectosSerializer(proyectos, many=False, context=serializer_context)
        return Response(serializer.data)


class EventosList(APIView):
    def get(self, request):
        serializer_context = {
            'request': request,
        }
        eventos = Eventos.objects.all()
        serializer = EventosSerializer(eventos, many=True, context=serializer_context)
        return Response(serializer.data)

class ProjectEvents(APIView):
    def get(self, request, id_proyecto, fecha_inicio, fecha_final):
        serializer_context = {
            'request': request,
        }

        string_fecha_inicio = fecha_inicio + " 12:00:00"
        date_inicio = datetime.datetime.strptime(string_fecha_inicio, "%d-%m-%Y %H:%M:%S")
        
        string_fecha_final = fecha_final + " 12:00:00"
        date_final = datetime.datetime.strptime(string_fecha_final, "%d-%m-%Y %H:%M:%S")

        eventos = Eventos.objects.filter(descripcion__contains=id_proyecto, inicio__range=[date_inicio, date_final])

        personas = Persona.objects.all()

        diccionario = {}
        for evento in eventos:
            diccionario[evento.id_persona.id] = 0

        for evento in eventos:
            diferencia = evento.termino-evento.inicio
            total_horas = diferencia.total_seconds()/3600
            diccionario[evento.id_persona.id]+=total_horas

        for key in diccionario:
            for persona in personas:
                if key==persona.id:
                    diccionario[persona.nombre] = diccionario[persona.id]
                    del diccionario[persona.id]
        
        lista = []
        for key in diccionario:
            diccionario_nuevo = {}
            diccionario_nuevo['nombre'] = key
            diccionario_nuevo['horas'] = diccionario[key]
            lista.append(diccionario_nuevo)

        serializer = HorasProyectoSerializer(lista, many=True, context=serializer_context)
        return Response(serializer.data)

class PersonEvents(APIView):
    def get(self, request, id_persona, fecha_inicio, fecha_final):
        serializer_context = {
            'request': request,
        }
        
        string_fecha_inicio = fecha_inicio + " 12:00:00"
        date_inicio = datetime.datetime.strptime(string_fecha_inicio, "%d-%m-%Y %H:%M:%S")
        
        string_fecha_final = fecha_final + " 12:00:00"
        date_final = datetime.datetime.strptime(string_fecha_final, "%d-%m-%Y %H:%M:%S")

        eventos = Eventos.objects.filter(id_persona=id_persona, inicio__range=[date_inicio, date_final])

        proyectos = Proyectos.objects.all()

        diccionario_proyectos = {}
        diccionario_tipo_trabajo = {"Reunión":0, "Trabajo individual":0, "Otros":0}
        for evento in eventos:
            for proyecto in proyectos:
                if proyecto.id in evento.descripcion:
                    diccionario_proyectos[proyecto.nombre] = 0

        for evento in eventos:
            diferencia = evento.termino-evento.inicio
            total_horas = diferencia.total_seconds()/3600
            if "Otros" in evento.descripcion or "Otros" in evento.titulo:
                diccionario_tipo_trabajo["Otros"]+=total_horas
            elif evento.participantes == 0 or "[P]" in evento.titulo or "[p]" in evento.titulo or "Trabajo individual" in evento.titulo:
                diccionario_tipo_trabajo["Trabajo individual"]+=total_horas
            elif evento.participantes>=1 or "Reunión" in evento.titulo:
                diccionario_tipo_trabajo["Reunión"]+=total_horas
            for proyecto in proyectos:
                if proyecto.id in evento.descripcion:
                    diccionario_proyectos[proyecto.nombre] += total_horas

        lista = []
        dicc_1_final = {"proyectos":diccionario_proyectos, "tipo_trabajo":diccionario_tipo_trabajo}
        lista.append(dicc_1_final)
        
        serializer = HorasPersonaSerializer(lista, many=True, context=serializer_context)
        return Response(serializer.data)

class AreaMeetings(APIView):
    def get(self, request, fecha_inicio, fecha_final):
        serializer_context = {
            'request': request,
        }

        string_fecha_inicio = fecha_inicio + " 12:00:00"
        date_inicio = datetime.datetime.strptime(string_fecha_inicio, "%d-%m-%Y %H:%M:%S")
        
        string_fecha_final = fecha_final + " 12:00:00"
        date_final = datetime.datetime.strptime(string_fecha_final, "%d-%m-%Y %H:%M:%S")

        all_eventos = Eventos.objects.filter(inicio__range=[date_inicio, date_final])
        meetings_eventos = Eventos.objects.filter(Q(titulo__icontains="Reunión")| Q(participantes__gte=1), inicio__range=[date_inicio, date_final])

        diccionario_areas_reuniones = {}
        diccionario_areas_total_horas = {}
        
        for evento in all_eventos:
            diccionario_areas_total_horas[evento.id_persona.area] = 0
            diccionario_areas_reuniones[evento.id_persona.area] = 0

        
        for evento in all_eventos:
            diferencia = evento.termino-evento.inicio
            total_horas = diferencia.total_seconds()/3600
            diccionario_areas_total_horas[evento.id_persona.area]+=total_horas

        for evento in meetings_eventos:
            diferencia = evento.termino-evento.inicio
            total_horas = diferencia.total_seconds()/3600
            diccionario_areas_reuniones[evento.id_persona.area]+=total_horas
        
        diccionario_final = {"estadisticas":[]}
        for key in diccionario_areas_total_horas:
            diccionario  = {}
            diccionario[key] = (diccionario_areas_reuniones[key]/diccionario_areas_total_horas[key])*100
            diccionario_final["estadisticas"].append(diccionario)
            
        serializer = EstadisticasAreasSerializer(diccionario_final, context=serializer_context)
        return Response(serializer.data)

class EventsByType(APIView):
    def get(self, request, fecha_inicio, fecha_final):
        serializer_context = {
            'request': request,
        }

        string_fecha_inicio = fecha_inicio + " 12:00:00"
        date_inicio = datetime.datetime.strptime(string_fecha_inicio, "%d-%m-%Y %H:%M:%S")
        
        string_fecha_final = fecha_final + " 12:00:00"
        date_final = datetime.datetime.strptime(string_fecha_final, "%d-%m-%Y %H:%M:%S")

        
        all_eventos = Eventos.objects.filter(inicio__range=[date_inicio, date_final])
        ## Eventos de las personas en los que trabajen solos
        espacios_trabajo = Eventos.objects.filter((Q(titulo__icontains="[P]")| Q(titulo__icontains="[p]")) & Q(participantes=0), inicio__range=[date_inicio, date_final])
        ## Eventos de las personas en las que asisten a reuniones
        reuniones = Eventos.objects.filter(Q(titulo__icontains="Reunión")| Q(participantes__gte=1), inicio__range=[date_inicio, date_final])

        diccionario_tipo_trabajo = {"Reuniones":0, "Espacio de trabajo": 0, "Espacio libre":0}
        total_horas_general = 0
        total_horas_reuniones = 0
        total_horas_espacio_trabajo = 0
        
        
        for evento in all_eventos:
            diferencia = evento.termino-evento.inicio
            total_horas = diferencia.total_seconds()/3600
            total_horas_general+= total_horas

        for evento in espacios_trabajo:
            diferencia = evento.termino-evento.inicio
            total_horas = diferencia.total_seconds()/3600
            total_horas_espacio_trabajo+= total_horas

        for evento in reuniones:
            diferencia = evento.termino-evento.inicio
            total_horas = diferencia.total_seconds()/3600
            total_horas_reuniones+= total_horas

        total_horas_libre = total_horas_general - total_horas_reuniones - total_horas_espacio_trabajo

        diccionario_tipo_trabajo["Reuniones"] = round((total_horas_reuniones/total_horas_general) * 100, 2)
        diccionario_tipo_trabajo["Espacio de trabajo"] = round((total_horas_espacio_trabajo/total_horas_general) * 100, 2)
        diccionario_tipo_trabajo["Espacio libre"]  = round((total_horas_libre/total_horas_general) * 100, 2)

        diccionario_final ={"tipo_trabajo": diccionario_tipo_trabajo}

        serializer = TipoTrabajoSerializer(diccionario_final, context=serializer_context)
        return Response(serializer.data)