import eel
import matplotlib.pyplot as plt
import io
import base64
from web.message_binaire.message_binaire import get_stored_message
import random


def generate_clock(period, num_bits):
    vect = []
    if period % 2 == 0:  # Si la période est paire
        for _ in range(num_bits):
            j = 0
            while j < (period / 2):
                vect.append(1)
                j += 1
            j = 0  # Remettre j à 0 pour la deuxième boucle
            while j < (period / 2):
                vect.append(-1)
                j += 1
    else:  # Si la période est impaire
        for _ in range(num_bits):
            j = 0
            while j <= (period / 2):
                vect.append(1)
                j += 1  # Incrémenter j de la moitié de la période
            j = 0  # Remettre j à 0 pour la deuxième boucle
            while j <= (period / 2 ):
                vect.append(-1)
                j += 1
    return vect





####################################################################################
########################    definition des codes    ###############################

def nrz_encode(binary_code):
    encoded_signal = []
    for bit in binary_code:
        if bit == '0':
            encoded_signal.append(-1)  # Assign -1 for '0'
        elif bit == '1':
            encoded_signal.append(1)   # Assign +1 for '1'
    return encoded_signal

def rz_encode(binary_code):
    encoded_signal = []
    for bit in binary_code:
            if bit == '0':
                encoded_signal.append(0)  # Assign 0 for '0'
            elif bit == '1':
                encoded_signal.extend([1, 0])   
    return encoded_signal

def manchester_encode(binary_code):
    encoded_signal = []
    for bit in binary_code:
            if bit == '1':
                encoded_signal.extend([1, -1])  # Pour '0', on émet d'abord un signal haut puis bas
            elif bit == '0':
                encoded_signal.extend([-1, 1])  # Pour '1', on émet d'abord un signal bas puis haut
    return encoded_signal

def miller_encode(binary_code):
        encoded_signal = []
        state = 1  # État initial
        prev_bit = '1'  # Initialisation du bit précédent

        for bit in binary_code:
            if bit == '1':
                encoded_signal.extend([state, -state])  # Transition de haut à bas
                state = -state
                prev_bit = '1'
            elif bit == '0':
                if prev_bit == '1':
                    encoded_signal.extend([state,state])  # Maintien du niveau bas pour les bits nuls
                    prev_bit = '0'
                elif prev_bit == '0':    
                    encoded_signal.extend([-state,-state])  # Transition entre les bits nuls
                    state = -state  # Inversion de l'état pour chaque bit
                    prev_bit = '0'
        return encoded_signal            

def encodeur_hdbn(seq_bin , n):
    encoded_signal = []
    encoded_signal1 = []
    state = 1
    nbr_zero = 0
    frst__V=1
    state_v =0
    prev_bit ='1'
    
    for bit in seq_bin:
        if bit == '1':
            encoded_signal.append(state)
            if frst__V ==1:
                state_v=state
            state = - state
            prev_bit = bit
            nbr_zero = 1
            
        if bit == '0' :
            if nbr_zero == n :
                frst__V = 5
                encoded_signal.append(state_v)
                state_v=-state_v
                nbr_zero = 0
            else :    
                encoded_signal.append(0) 
                if prev_bit == '0' : 
                    nbr_zero =nbr_zero + 1
            prev_bit = bit   
            
            
    encoded_signal_int = [int(bit) for bit in encoded_signal]  
    last_state = 0 
    nbr_zero = 0
    prev_bit = 1
    frst__V=1
    for bit in encoded_signal_int:
        if bit == 0 :
            if prev_bit == 1  and nbr_zero == n-1  :
                if frst__V == 1 :
                    encoded_signal1.append(bit)
                    nbr_zero = 0 
                    frst__V = 5
                else :    
                    encoded_signal1.append(-last_state)
                    nbr_zero = 0 
            else :
                encoded_signal1.append(bit)    
                
            if prev_bit == 0 :
                nbr_zero = nbr_zero + 1 
                
            prev_bit = 0
            
            
        if bit == 1 or bit  == -1 :
            encoded_signal1.append(bit)
            prev_bit = 1 
            last_state = bit 
            
            if nbr_zero !=  n-1 :
                nbr_zero = 0
            

             
    return encoded_signal1

####################################################################################
########################        plot des codes       ###############################

def plot_clock_and_nrz(period, binary_code):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))  # Créez une figure avec deux sous-graphiques

    # Tracer le signal d'horloge
    clock_period = generate_clock(period=period, num_bits=len(binary_code))  # Crée un cycle d'horloge de période 1
    clock = []  # Initialise une liste pour stocker les valeurs du signal d'horloge
    for i in range(0, len(binary_code) * period, period):
        clock.extend(clock_period)  # Étend la liste avec un cycle d'horloge
    ax1.step(range(0, len(clock)), clock, where='post', label='Clock Signal')
    ax1.set_ylim(-0.2, 1.2)  # Set y-axis limits to accommodate signal values
    ax1.set_xlim(0, len(binary_code) * period)  # Définir la plage de l'axe des x en fonction de la longueur du message binaire et de la période
    ax1.set_xlabel('Bit Index')
    ax1.set_ylabel('Voltage Level')
    ax1.set_title('Clock Signal')
    ax1.grid(True)

    # Tracer le signal NRZ
    encoded_signal_1 = nrz_encode(binary_code)
    encoded_signal = []
    for bit in encoded_signal_1:
        encoded_signal.extend([int(bit)] * period)
    
    ax2.step(range(0, len(encoded_signal)), encoded_signal, where='post', label='NRZ Signal')
    ax2.set_ylim(-1.5, 1.5)  # Set y-axis limits to accommodate signal values
    ax2.set_xlim(0, len(binary_code)* period)
    ax2.set_xlabel('Bit Index')
    ax2.set_ylabel('Voltage Level')
    ax2.set_title('NRZ Signal')
    ax2.grid(True)

    # Ajouter de l'espace entre les sous-graphiques
    plt.tight_layout()

    # Convertir le plot en image
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.read()).decode('utf-8')
    plt.close()

    return img_str


def plot_clock_and_rz(period, binary_code):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))  # Créez une figure avec deux sous-graphiques

    # Tracer le signal d'horloge
    clock_period = generate_clock(period=period, num_bits=len(binary_code))  # Crée un cycle d'horloge de période 1
    clock = []  # Initialise une liste pour stocker les valeurs du signal d'horloge
    for i in range(0, len(binary_code) * period, period):
        clock.extend(clock_period)  # Étend la liste avec un cycle d'horloge
    ax1.step(range(0, len(clock)), clock, where='post', label='Clock Signal')
    ax1.set_ylim(-0.2, 1.2)  # Set y-axis limits to accommodate signal values
    ax1.set_xlim(0, len(binary_code) * period)  # Définir la plage de l'axe des x en fonction de la longueur du message binaire et de la période
    ax1.set_xlabel('Bit Index')
    ax1.set_ylabel('Voltage Level')
    ax1.set_title('Clock Signal')
    ax1.grid(True)

    # Tracer le signal NRZ
    encoded_signal_1 = rz_encode(binary_code)
    encoded_signal = []
    for i, bit in enumerate(encoded_signal_1):
        if i < len(encoded_signal_1) :
            if bit == 1 and encoded_signal_1[i+1] == 0:
                encoded_signal.extend([int(bit)] * int(period/2))
            elif bit == 0 and encoded_signal_1[i-1] == 1:
                encoded_signal.extend([int(bit)] * int(period/2)) 
            else  :       
                encoded_signal.extend([int(bit)] * period)

        
    ax2.step(range(0, len(encoded_signal)), encoded_signal, where='post', label='RZ Signal')
    ax2.set_ylim(-1.5, 1.5)  # Set y-axis limits to accommodate signal values
    ax2.set_xlim(0, (len(binary_code)* period ))
    ax2.set_xlabel('Bit Index')
    ax2.set_ylabel('Voltage Level')
    ax2.set_title('RZ Signal')
    ax2.grid(True)

    # Ajouter de l'espace entre les sous-graphiques
    plt.tight_layout()

    # Convertir le plot en image
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.read()).decode('utf-8')
    plt.close()

    return img_str


def plot_clock_and_manchester(period, binary_code):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))  # Créez une figure avec deux sous-graphiques

    # Tracer le signal d'horloge
    clock_period = generate_clock(period=period, num_bits=len(binary_code))  # Crée un cycle d'horloge de période 1
    clock = []  # Initialise une liste pour stocker les valeurs du signal d'horloge
    for i in range(0, len(binary_code) * period, period):
        clock.extend(clock_period)  # Étend la liste avec un cycle d'horloge
    ax1.step(range(0, len(clock)), clock, where='post', label='Clock Signal')
    ax1.set_ylim(-0.2, 1.2)  # Set y-axis limits to accommodate signal values
    ax1.set_xlim(0, len(binary_code) * period)  # Définir la plage de l'axe des x en fonction de la longueur du message binaire et de la période
    ax1.set_xlabel('Bit Index')
    ax1.set_ylabel('Voltage Level')
    ax1.set_title('Clock Signal')
    ax1.grid(True)


    # Tracer le signal NRZ
    encoded_signal_1 = manchester_encode(binary_code)
    encoded_signal = []
    for bit in encoded_signal_1:
        encoded_signal.extend([int(bit)] * int(period/2))
        
    ax2.step(range(0, len(encoded_signal)), encoded_signal, where='post', label='manchester Signal')
    ax2.set_ylim(-1.5, 1.5)  # Set y-axis limits to accommodate signal values
    ax2.set_xlim(0, len(binary_code)* period)
    ax2.set_xlabel('Bit Index')
    ax2.set_ylabel('Voltage Level')
    ax2.set_title('manchester Signal')
    ax2.grid(True)

    # Ajouter de l'espace entre les sous-graphiques
    plt.tight_layout()

    # Convertir le plot en image
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.read()).decode('utf-8')
    plt.close()

    return img_str



def plot_clock_and_miller(period, binary_code):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))  # Créez une figure avec deux sous-graphiques

    # Tracer le signal d'horloge
    clock_period = generate_clock(period=period, num_bits=len(binary_code))  # Crée un cycle d'horloge de période 1
    clock = []  # Initialise une liste pour stocker les valeurs du signal d'horloge
    for i in range(0, len(binary_code) * period, period):
        clock.extend(clock_period)  # Étend la liste avec un cycle d'horloge
    ax1.step(range(0, len(clock)), clock, where='post', label='Clock Signal')
    ax1.set_ylim(-0.2, 1.2)  # Set y-axis limits to accommodate signal values
    ax1.set_xlim(0, len(binary_code) * period)  # Définir la plage de l'axe des x en fonction de la longueur du message binaire et de la période
    ax1.set_xlabel('Bit Index')
    ax1.set_ylabel('Voltage Level')
    ax1.set_title('Clock Signal')
    ax1.grid(True)


    # Tracer le signal miller
    encoded_signal_1 = miller_encode(binary_code)
    encoded_signal = []
    for bit in encoded_signal_1:
        encoded_signal.extend([int(bit)] * int(period/2))
     
    B_n = []    
    for i in range(0,len(binary_code))  :
        B_n.append(int(binary_code[i]))    
    
    # Code pour déterminer le point de départ sur l'axe des x
    if B_n[0] == 0 :
        start_point = int(period/2)    
    else :
        start_point = 0
    
    
    ax2.step(
    [start_point + i for i in range(len(encoded_signal))], 
    encoded_signal, 
    where='post', 
    label='Signal Miller'
    )
    ax2.set_ylim(-1.5, 1.5)  # Définir les limites de l'axe y pour accueillir les valeurs du signal
    ax2.set_xlim(0, len(binary_code) * period)
    ax2.set_xlabel('Index du bit')
    ax2.set_ylabel('Niveau de tension')
    ax2.set_title('Signal Miller')
    ax2.grid(True)

    # Ajouter de l'espace entre les sous-graphiques
    plt.tight_layout()

    # Convertir le plot en image
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.read()).decode('utf-8')
    plt.close()

    return img_str


def plot_clock_and_hdb(period, binary_code , userInput):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))  # Créez une figure avec deux sous-graphiques

    # Tracer le signal d'horloge
    clock_period = generate_clock(period=period, num_bits=len(binary_code))  # Crée un cycle d'horloge de période 1
    clock = []  # Initialise une liste pour stocker les valeurs du signal d'horloge
    for i in range(0, len(binary_code) * period, period):
        clock.extend(clock_period)  # Étend la liste avec un cycle d'horloge
    ax1.step(range(0, len(clock)), clock, where='post', label='Clock Signal')
    ax1.set_ylim(-0.2, 1.2)  # Set y-axis limits to accommodate signal values
    ax1.set_xlim(0, len(binary_code) * period)  # Définir la plage de l'axe des x en fonction de la longueur du message binaire et de la période
    ax1.set_xlabel('Bit Index')
    ax1.set_ylabel('Voltage Level')
    ax1.set_title('Clock Signal')
    ax1.grid(True)

    # Tracer le signal NRZ
    encoded_signal_1 = encodeur_hdbn(binary_code , userInput)
    encoded_signal = []
    for bit in encoded_signal_1:
        encoded_signal.extend([int(bit)] * period)
    ax2.step(range(0, len(encoded_signal)), encoded_signal, where='post', label='hdbn Signal')
    ax2.set_ylim(-1.5, 1.5)  # Set y-axis limits to accommodate signal values
    ax2.set_xlim(0, len(binary_code)* period)
    ax2.set_xlabel('Bit Index')
    ax2.set_ylabel('Voltage Level')
    ax2.set_title('hdb3 Signal')
    ax2.grid(True)

    # Ajouter de l'espace entre les sous-graphiques
    plt.tight_layout()

    # Convertir le plot en image
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.read()).decode('utf-8')
    plt.close()

    return img_str


def handle_selected_option(option, ts_value, message=None , userInput=None):
 
    if message is None:
        message = get_stored_message()  # Utilisez la variable globale si message n'est pas spécifié
    binary_code = message  
    if option == "NRZ":
        plot_img = plot_clock_and_nrz(int(ts_value), binary_code)
        return { 'plot_img': plot_img}
    elif option == "RZ":
        plot_img = plot_clock_and_rz(int(ts_value), binary_code)
        return { 'plot_img': plot_img}
    elif option == "Manchester":
        plot_img = plot_clock_and_manchester(int(ts_value), binary_code)
        return { 'plot_img': plot_img}
    elif option == "Miller":
        plot_img = plot_clock_and_miller(int(ts_value), binary_code)
        return { 'plot_img': plot_img}
    elif option == "bipolaires (HDBn)":
        plot_img = plot_clock_and_hdb(int(ts_value), binary_code , userInput)
        return { 'plot_img': plot_img}


#Génère une chaîne binaire aléatoire de la longueur spécifiée.
def generate_random_binary():

    # Génère une longueur aléatoire entre 5 et 15
    length = random.randint(5, 15)
    binary_string = ""
    for _ in range(length):
        # Ajoute aléatoirement 0 ou 1 à la chaîne binaire
        binary_string += str(random.randint(0, 1))
    return binary_string

def ouvrir_codeur_enligne():
    # Port  utiliser pour la nouvelle fenêtre
    new_port = 8080  

    # Ouvrir la nouvelle fenêtre en spécifiant le port
    eel.init('web')  # Dossier contenant votre fichier HTML, CSS, JavaScript
    eel.start('codeur_enligne/codeur_enligne.html',  port=new_port)

