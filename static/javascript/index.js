// Verifica si la página se recargó
if (sessionStorage.getItem("reloaded")) {
    // Si la página se recargó, borra los mensajes flash
    const flashMessages = document.querySelectorAll('.flash-messages .alert');
    flashMessages.forEach(function(message) {
        message.style.display = 'none';
    });
    sessionStorage.removeItem("reloaded");
}

// Cuando el usuario intente recargar la página, establece la variable de recarga
window.onbeforeunload = function() {
    sessionStorage.setItem("reloaded", "true");
};

