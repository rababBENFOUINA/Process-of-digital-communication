import eel


def ouvrir_entrer_message():
    # Port  utiliser pour la nouvelle fenêtre
    new_port = 8080  

    # Ouvrir la nouvelle fenêtre en spécifiant le port
    eel.init('web')  # Dossier contenant votre fichier HTML, CSS, JavaScript
    eel.start('message_binaire/entrer_message.html',  port=new_port)


# Définition de la fonction save_message
stored_message = None


def set_stored_message(value):
    global stored_message
    stored_message = value


def save_stored_message():
    global stored_message
    print("Variable globale enregistrée :", stored_message)
        
def get_stored_message():
    return stored_message
