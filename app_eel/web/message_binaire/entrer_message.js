eel.init();

// Obtenez la taille de l'écran
var screenWidth = window.screen.width;
var screenHeight = window.screen.height;

// Définissez la taille de la fenêtre
var windowWidth = 500;
var windowHeight = 500;

// Calculez la position pour centrer la fenêtre
var leftPosition = (screenWidth - windowWidth) / 2;
var topPosition = (screenHeight - windowHeight) / 2;

// Redimensionner et positionner la fenêtre
window.resizeTo(windowWidth, windowHeight);
window.moveTo(leftPosition, topPosition);


function submitForm() {
    // Récupérer la valeur de l'input
    var messageInput = document.getElementById('message').value;
    
    // Appeler une fonction Python via Eel et lui passer la valeur de l'input
    eel.set_stored_message(messageInput)();
    
    // Enregistrer la variable globale
    eel.save_stored_message();
    
    // Fermer la fenêtre
    window.close();
    
    // Empêcher le formulaire de se soumettre normalement
    return false;
}

function generateRandomBinary() {
    eel.generate_random_binary()(function (result) {
        console.log("Chaîne binaire aléatoire générée :", result);
        // Sélectionner l'élément input
        var outputElement = document.getElementById("message");
        // Assigner la valeur résultante à l'élément input
        outputElement.value = result;
    });
}
