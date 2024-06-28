document.addEventListener('DOMContentLoaded', function () {
    const modalInformacion = document.getElementById('modalInformacion');
    modalInformacion.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const hotelId = button.getAttribute('data-id');

        fetch(`/get_hotel_info/${hotelId}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error fetching data');
                }
                return response.json();
            })
            .then(data => {
                document.getElementById('hotelNombre').textContent = data.nombre;
                document.getElementById('hotelUbicacion').textContent = data.ubicacion;
                document.getElementById('hotelCantidadHabitaciones').textContent = data.cantidad_habitaciones;
                document.getElementById('hotelTiposHabitacion').textContent = data.tipos_habitacion;

                // Botón Editar
                document.getElementById('btnEditar').onclick = function() {
                    window.location.href = `/editar_hotel/${hotelId}/`;
                };

                // Botón Eliminar
                document.getElementById('btnEliminar').onclick = function() {
                    if (confirm('¿Estás seguro de que quieres eliminar este hotel?')) {
                        const formEliminar = document.getElementById('form-eliminar');
                        formEliminar.action = `/eliminar_hotel/${hotelId}/`;
                        formEliminar.submit();
                    }
                };
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    });
});
