# Laboratorio1_Gestion_de_cines
# 🎬 Laboratorio1_Gestion_de_cines

Proyecto desarrollado en Django REST Framework que simula un sistema de gestión de cines. Permite a los usuarios consultar funciones disponibles, reservar entradas y gestionar salas, películas y horarios. Está enfocado en la implementación de una API RESTful para el manejo de recursos relacionados con la cartelera de cine.

## 🚀 Descripción general

Este sistema permite:

- Registrar funciones de películas en salas específicas.
- Consultar películas, salas, tipos de formato y horarios disponibles.
- Permitir que un usuario realice una reserva indicando función, cantidad de entradas y asientos.
- Registrar asientos reservados y calcular el precio total.
- Validar que los asientos seleccionados no estén ocupados.
- Garantizar la integridad de los datos mediante validaciones personalizadas.

##  Modelos principales

###  Película (`Pelicula`)
- `titulo`: Título de la película.
- `descripcion`: Descripción general.
- `duracion`: Duración en minutos.
- `clasificacion`: Clasificación por edad.

###  Sala (`Sala`)
- `nombre`: Nombre de la sala.
- `capacidad`: Cantidad total de asientos.

###  Tipo de Formato (`TipoFormato`)
- `nombre`: Nombre del formato (2D, 3D, IMAX, etc).
- `precio_adicional`: Costo extra según el tipo de formato.

###  Función (`Funcion`)
- `pelicula`: Película proyectada.
- `sala`: Sala asignada.
- `tipo_formato`: Formato de proyección.
- `fecha`: Fecha de la función.
- `hora`: Hora de inicio.
- `activa`: Booleano que indica si la función está activa.

###  Reserva (`Reserva`)
- `usuario`: Usuario que realiza la reserva.
- `funcion`: Función a la que se reserva.
- `cantidad_entradas`: Número de entradas.
- `precio_total`: Precio calculado de la reserva.
- `asientos_reservados`: Asientos seleccionados para esa función.

###  Asiento (`Asiento`)
- `sala`: Sala a la que pertenece.
- `numero`: Número identificador del asiento.

###  AsientoReservado
- `reserva`: Reserva asociada.
- `asiento`: Asiento específico.
- `funcion`: Función a la que corresponde.

##  Requisitos del API

###  Endpoints

- `GET /api/pelicula/` — Listado de películas.
- `GET /api/funcion/` — Listado de funciones activas.
- `POST /api/reserva/` — Crear una reserva (enviando IDs de función y asientos).
- `GET /api/sala/` — Consulta de salas disponibles.
- `GET /api/tipo-formato/` — Consulta de tipos de formato.

### 🔸 Requisitos para POST `/api/reservas/`

```json
{
  "funcion_id": 2,
  "cantidad_entradas": 2,
  "asientos": [4, 5]
}
