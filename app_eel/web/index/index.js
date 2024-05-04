 // Attendez que le DOM soit chargé
 document.addEventListener("DOMContentLoaded", function() {
    // Sélectionnez le bouton par son ID
    var btnOpen = document.getElementById("btn-open");

    // Ajoutez un écouteur d'événements de clic au bouton
    btnOpen.addEventListener("click", function() {
        // Appel à la fonction exposée de Python pour ouvrir une nouvelle fenêtre
        eel.ouvrir_entrer_message();
    });
});

 // Attendez que le DOM soit chargé
 document.addEventListener("DOMContentLoaded", function() {
    // Sélectionnez le bouton par son ID
    var btnOpen = document.getElementById("codeur_enligne");

    // Ajoutez un écouteur d'événements de clic au bouton
    btnOpen.addEventListener("click", function() {
        // Appel à la fonction exposée de Python pour ouvrir une nouvelle fenêtre
        eel.ouvrir_codeur_enligne();
    });
});
