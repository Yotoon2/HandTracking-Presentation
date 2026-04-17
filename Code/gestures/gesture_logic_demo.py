import time
from pynput import keyboard
from pynput.mouse import Button, Controller
m = Controller() #Pour controller la souris
controller = keyboard.Controller() #Pour contrôller le clavier

seuilBas = 100
seuilHaut = 210
prev_gz = 0

SEUIL = 100
COOLDOWN = 5
last_trigger = 0
ZONE_MORTE = 25
history = []

def detect_pos_flex(flex):

    flex = transform_flex(flex)

    match flex:
        case [0, 0, 0]:
            return "ouvert"
        case [2, 2, 2]:
            return "poing"
        
        case [1, 1, 2]:
            return "pince"
        
        case [2, 0, 0]:
            return "swipe"
        case [2, 1, 1]:
            return "swipe"
        case [2, 1, 0]:
            return "swipe"
        case [2, 0, 1]:
            return "swipe"
    
    return "none"

def transform_flex(flex):
    string = str(flex)
    for i in range(len(flex)):
        if flex[2] == 0:
            flex[2] = flex[1]
        if flex[i] > seuilHaut:
            flex[i] = "tendu"
        elif flex[i] > seuilBas:
            flex[i] = "fléchi"
        else:
            flex[i] = "fermé"
    print(string + " -> " + str(flex))
    return flex

def detect_gesture(acc, gyro, magneto, flex_str):
    global history
    gz = gyro[2]
    #print(gz)

    history.append(gz)
    if len(history) > 5:
        history.pop(0)
    if flex_str != "swipe":
        return None
    
    if max(history) > 80:
        history.clear()
        return "swipe_droit"
    if min(history) < -80:
        history.clear
        return "swipe_gauche"



def get_thumb_direction(landmarks):
    """
    Fonction afin de savoir la direction du pouce lorsque qu'un geste "pouce à l'horizontal" est détecté.
    Le modèle hésite trop à faire lui-même la différence entre gauche/droite donc on se sert des landmarks (points sur les doigts)
    """

    thumb_x = landmarks[4].x
    index_x = landmarks[5].x

    if thumb_x > index_x:
        return "thumb_left"
    else:
        return "thumb_right"