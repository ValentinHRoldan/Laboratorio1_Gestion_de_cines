from rest_framework import routers
from apps.funciones.api import PeliculaViewSet, FuncionViewSet, SalaViewSet
from apps.reservas.api import ReservaViewSet

# Initializar el router de DRF solo una vez
router = routers.DefaultRouter()

# Registrar un ViewSet
router.register(prefix='pelicula', viewset=PeliculaViewSet)
router.register(prefix='funcion', viewset=FuncionViewSet)
router.register(prefix='sala', viewset=SalaViewSet)

router.register(prefix='reserva', viewset=ReservaViewSet)