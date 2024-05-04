import eel
import tkinter as tk
from web.message_binaire import message_binaire
from web.codeur_enligne import codeur_enligne

# Définir la taille de la fenêtre
window_width = 1000
window_height = 700

# Créer une fenêtre factice tkinter pour obtenir la taille de l'écran
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()  # Fermer la fenêtre factice

# Calculer la position pour centrer la fenêtre
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

# Initialiser Eel
eel.init('web')

#--------------entrer_message----------------
# Exposer les fonctions
eel.expose(message_binaire.ouvrir_entrer_message)
eel.expose(message_binaire.save_stored_message)
eel.expose(message_binaire.set_stored_message)
eel.expose(message_binaire.get_stored_message)


#--------------entrer_message----------------
# Exposer les fonctions
eel.expose(codeur_enligne.ouvrir_codeur_enligne)
eel.expose(codeur_enligne.generate_clock)
eel.expose(codeur_enligne.nrz_encode)
eel.expose(codeur_enligne.plot_clock_and_nrz)
eel.expose(codeur_enligne.handle_selected_option)
eel.expose(codeur_enligne.generate_random_binary)

# Démarrer l'application Eel en utilisant les positions calculées
eel.start('index/index.html', size=(window_width, window_height), position=(x_position, y_position))
