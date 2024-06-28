document.addEventListener('DOMContentLoaded', function () {
    const modalInformacion = document.getElementById('modalInformacion');
    modalInformacion.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const habitacionId = button.getAttribute('data-id');

        fetch(`/get_habitacion_info/${habitacionId}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error fetching data');
                }
                return response.json();
            })
            .then(data => {
                document.getElementById('habitacionTipo').textContent = data.tipo_habitacion;
                document.getElementById('habitacionCantidadPersonas').textContent = data.cantidad_personas;
                document.getElementById('habitacionCamas').textContent = data.camas;
                document.getElementById('habitacionBanos').textContent = data.banos;
                document.getElementById('habitacionPrecio').textContent = data.precio_por_dia;
                document.getElementById('habitacionDisponible').textContent = data.disponible ? 'Sí' : 'No';
                document.getElementById('habitacionDescripcion').textContent = data.descripcion;

                // Botón Editar
                document.getElementById('btnEditar').href = `/habitaciones/editar/${habitacionId}/`;

                // Botón Eliminar
                document.getElementById('btnEliminar').href = `/habitaciones/eliminar/${habitacionId}/`;
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    });
});