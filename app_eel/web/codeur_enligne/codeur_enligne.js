function sendDataToPython() {
    var selectedOption = document.querySelector('input[name="codage"]:checked').value;
    var tsValue = document.getElementById('message').value;
    var userInput = null; // Initialiser userInput à null

    // Vérifier si l'option est "bipolaires (HDBn)"
    if (selectedOption === "bipolaires (HDBn)") {
        var attempts = 3; // Nombre de tentatives autorisées
        
        for (var i = 0; i < attempts; i++) {
            // Demander à l'utilisateur de saisir une valeur pour HDBn
            var userInputString = prompt("Veuillez saisir une valeur pour HDBn (tentative " + (i+1) + " sur " + attempts + "):");
            
            // Convertir la valeur saisie en entier
            userInput = parseInt(userInputString);
            
            // Vérifier si la conversion a réussi
            if (!isNaN(userInput)) {
                // Sortir de la boucle si la saisie est valide
                break;
            } else {
                // Afficher un message d'erreur si la saisie n'est pas valide
                if (i < attempts - 1) {
                    alert("Veuillez saisir une valeur numérique valide pour HDBn.");
                } else {
                    // Afficher un message d'erreur sans la possibilité de saisie après la dernière tentative
                    alert("Vous avez dépassé le nombre de tentatives autorisées. Veuillez réessayer plus tard.");
                    return;
                }
            }
        }
    }



    // Récupérer la valeur de la chaîne et vérifier sa validité
    var input = document.getElementById("chaine").value;
    var regex = /^[01]*$/;  // Autoriser une entrée vide ou une liste de 0 et de 1

    // Si l'entrée n'est pas vide et ne correspond pas à la validation regex
    if (input !== "" && !regex.test(input)) {
        alert("Entrez uniquement une liste de 0 et de 1.");
        return;
    }

    // Appeler la fonction Python avec les données validées
    eel.handle_selected_option(selectedOption, tsValue, input, userInput)(function (response) {
        document.getElementById('plote').src = 'data:image/png;base64,' + response.plot_img;
    });
}

function afficherElement(type) {
    var contenu = document.getElementById("contenu");
    var boutonCodage = document.getElementById("boutonCodage");
    var boutonMessage = document.getElementById("boutonMessage");
    var input = document.getElementById("chaine").value;
    // Récupérer la taille de la div
    var tailleDiv = contenu.offsetWidth + "px";

    // Changer la taille de la div en fonction du bouton cliqué
    if (type === 'codage') {
        contenu.innerHTML = '<img id="plote" src="download.png" alt="NRZ Image">';
        contenu.style.width = tailleDiv;
        contenu.style.border = "1px solid black";
        boutonMessage.style.opacity = '0.5'; // Réduire l'opacité de l'autre bouton
        boutonCodage.style.opacity = '1'; // Rétablir l'opacité du bouton cliqué
        boutonMessage.style.backgroundColor = ''; // Réinitialiser la couleur de l'autre bouton
        boutonCodage.style.backgroundColor = 'rgba(108, 117, 125, 255)'; // Changer la couleur du bouton cliqué

        // Appel de la fonction sendDataToPython
        sendDataToPython();
    } else if (type === 'message') {
        contenu.innerHTML = '<p>Bienvenue sur notre plateforme de codage en ligne!</p>';
        contenu.style.width = tailleDiv;
        boutonCodage.style.opacity = '0.5'; // Réduire l'opacité de l'autre bouton
        boutonMessage.style.opacity = '1'; // Rétablir l'opacité du bouton cliqué
        boutonCodage.style.backgroundColor = ''; // Réinitialiser la couleur de l'autre bouton
        boutonMessage.style.backgroundColor = 'rgba(108, 117, 125, 255)'; // Changer la couleur du bouton cliqué
    }
}
