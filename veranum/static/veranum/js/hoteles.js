document.addEventListener('DOMContentLoaded', function () {
    const modalInformacion = document.getElementById('modalInformacion');
    modalInformacion.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const hotelId = button.getAttribute('data-id');
        const tipo_usuario = button.getAttribute('data-usuario');


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
                // Botón Editar
                document.getElementById('btnEditar').onclick = function() {
                    window.location.href = `/editar_hotel/${hotelId}/${tipo_usuario}/`;
                };

                // Botón Eliminar
                document.getElementById('btnEliminar').onclick = function() {
                    if (confirm('¿Estás seguro de que quieres eliminar este hotel?')) {
                        const formEliminar = document.getElementById('form-eliminar');
                        formEliminar.action = `/eliminar_hotel/${hotelId}/${tipo_usuario}/`;
                        formEliminar.submit();
                    }
                };
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const modalHabitaciones = document.getElementById('modalHabitaciones');
    modalHabitaciones.addEventListener('show.bs.modal', function (event) {
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
                const habitacionesContent = document.getElementById('habitacionesContent');
                habitacionesContent.innerHTML = '';

                console.log(data.habitaciones);

                data.habitaciones.forEach(habitacion => {
                    const habitacionElement = document.createElement('div');
                    habitacionElement.innerHTML = `
                        <h4>Habitación ${habitacion.numero_habitacion}</h4>
                        <p><strong>Precio por día:</strong> $${habitacion.precio_por_dia}</p>
                        <hr>
                    `;
                    habitacionesContent.appendChild(habitacionElement);
                });
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    });
});
