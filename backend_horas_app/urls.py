from django.urls import include, path
from . import views

urlpatterns = [
    path('personas/', views.PersonasList.as_view()),
    path('personas/<str:id>/', views.OnePerson.as_view()),
    path('proyectos/', views.ProyectosList.as_view()),
    path('proyectos/<str:id>/', views.OneProject.as_view()),
    path('eventos/', views.EventosList.as_view()),
    path('eventos/<str:id_proyecto>/<str:fecha_inicio>/<str:fecha_final>/', views.ProjectEvents.as_view()),
    path('eventos/personas/<str:id_persona>/<str:fecha_inicio>/<str:fecha_final>/', views.PersonEvents.as_view()),
    path('areas/reuniones/<str:fecha_inicio>/<str:fecha_final>/', views.AreaMeetings.as_view()),
    path('eventos/general/tipo_trabajo/<str:fecha_inicio>/<str:fecha_final>/', views.EventsByType.as_view()),

]