seuilBas = 100
seuilHaut = 210

def detect_gesture(flex):

    flex = transform_flex(flex)

    match flex:
        case [0, 0, 0]:
            print("ouvert")
            return "ouvert"
        
        case [2, 2, 2]:
            print("POING FERME")
            return "poing"
        
        case [1, 1, 2]:
            print("PINCE")
            return "pince"

    return "none"



def transform_flex(flex):
    print(flex)
    for i in range(len(flex)):
        if flex[i] > seuilHaut:
            flex[i] = 0
        elif flex[i] > seuilBas:
            flex[i] = 1
        else:
            flex[i] = 2
    print(flex)
    return flex

def transform_acc(acc):
    pass


def transform_gyro(gyro):
    pass

def transform_magneto(magneto):
    pass