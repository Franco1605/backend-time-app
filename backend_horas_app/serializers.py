from rest_framework import serializers

from .models import Persona, Proyectos, Eventos

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ('id', 'nombre', 'correo', 'password', 'area', 'id_calendario')

class ProyectosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyectos
        fields = ('id', 'nombre')

class EventosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eventos
        fields = ('id_persona', 'titulo', 'descripcion', 'participantes', 'inicio', 'termino')


class HorasProyectoSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=255)
    horas = serializers.CharField(max_length=255)


class HorasPersonaSerializer(serializers.Serializer):
    proyectos = serializers.JSONField()
    tipo_trabajo = serializers.JSONField()

class EstadisticasAreasSerializer(serializers.Serializer):
    estadisticas = serializers.JSONField()

class TipoTrabajoSerializer(serializers.Serializer):
    tipo_trabajo = serializers.JSONField()