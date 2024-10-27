// Función para iniciar el motor de inferencia mediante una solicitud HTTP
function iniciarMotor() {
    fetch('/iniciar_motor')
    .then(response => response.json())
    .then(data => {
        var recomendacionesDiv = document.getElementById('recomendaciones');
        recomendacionesDiv.innerHTML = '';  // Limpiamos recomendaciones previas
        data.forEach(function(mensaje) {
            var nuevaRecomendacion = document.createElement('p');
            nuevaRecomendacion.innerHTML = mensaje;
            recomendacionesDiv.appendChild(nuevaRecomendacion);
        });
    });
}
