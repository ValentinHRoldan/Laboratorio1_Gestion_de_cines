from django_filters import rest_framework as filters
from apps.funciones.models import Pelicula

class PeliculaFilter(filters.FilterSet):
    titulo = filters.CharFilter(field_name='titulo', lookup_expr='icontains')
    
class Meta:
    model = Pelicula
    fields = ['titulo']
