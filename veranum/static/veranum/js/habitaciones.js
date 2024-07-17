document.addEventListener('DOMContentLoaded', function () {
    const modalInformacion = document.getElementById('modalInformacion');
    modalInformacion.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const habitacionId = button.getAttribute('data-id');
        const tipo_usuario = button.getAttribute('data-usuario');

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
                const serviciosExtrasList = data.servicios_extras.split(',').map(servicio => {
                    return `<li>${servicio.trim()}</li>`;
                }).join('');
                document.getElementById('habitacionServicios').innerHTML = `<ul>${serviciosExtrasList}</ul>`;
                console.log(data);
                // Botón Editar
                document.getElementById('btnEditar').href = `/habitaciones/editar/${habitacionId}/${tipo_usuario}/`;

                // Botón Eliminar
                document.getElementById('btnEliminar').href = `/habitaciones/eliminar/${habitacionId}/"${tipo_usuario}"/`;
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    });
});
function cambiarDisponibilidad(habitacionId) {
    const url = `/cambiar-disponibilidad/${habitacionId}/`;
    const lista = ".lista" + habitacionId.toString();
    const fila = ".disponibilidad" + habitacionId.toString();
    console.log(lista);
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        console.log('Respuesta del servidor:', data);  // Verifica la respuesta del servidor
        
        if (data.status === 'success') {
            // Buscar la fila de la tabla correspondiente
            const row = document.querySelector(`${lista}`);
            console.log('Fila encontrada:', row);  // Verifica si se encuentra la fila
            
            if (row) {
                // Buscar la celda de disponibilidad en la posición correcta
                const disponibilidadTd = row.querySelector(`${fila}`);
                console.log('Celda de disponibilidad:', disponibilidadTd);  // Verifica la celda de disponibilidad
                
                if (disponibilidadTd) {
                    disponibilidadTd.innerHTML = data.disponible ? 'Sí' : 'No';
                } else {
                    console.error('No se encontró la celda de disponibilidad en la posición especificada.');
                }
            } else {
                console.error('No se encontró la fila con el ID especificado.');
            }
        } else {
            console.error('Error al cambiar la disponibilidad');
        }
    })
    .catch(error => console.error('Error:', error));
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function () {
    const modalHistorialPrecios = document.getElementById('modalHistorialPrecios');
    modalHistorialPrecios.addEventListener('show.bs.modal', function (event) {
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
                console.log('Historial de precios:', data.historial_precios);
                const historialPreciosList = document.getElementById('historialPreciosList');
                historialPreciosList.innerHTML = ''; // Limpiar contenido anterior
                
                // Dividir el string en un array usando coma como separador
                const preciosArray = data.historial_precios.split(',');

                // Iterar sobre el array de precios y agregar cada elemento a la lista
                preciosArray.forEach(precio => {
                    const precioItem = document.createElement('div');
                    precioItem.classList.add('precio-item');
                    // Si tienes un formato específico para fecha y precio, puedes separarlos
                    const [precioValue, fecha] = precio.trim().split(' - ');
                    precioItem.innerHTML = `
                        <p><strong>Fecha:</strong> ${fecha}</p>
                        <p><strong>Precio:</strong> ${precioValue}</p>
                    `;
                    historialPreciosList.appendChild(precioItem);
                });
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    });
});

