# Camera Hand-Tracking + Capteurs (projet CMI 2025-2026 umontpellier)

Ce projet-prototype a pour objectif la reconnaissance de gestes via hand-tracking (webcam) et via capteurs (hors webcam).
Il possède deux versions utilisable pour l'instant ; une considérant seulement du code python sans autre matériel (donc restriction à la webcam pour la détection de gestes) et l'autre ajoutant tout un montage avec capteurs flex sensors et carte arduino.

## Pré-requis
Il est nécessaire d'installer ces bibliothèques Arduino (sur IDE) pour exécuter les programmes avec la Arduino :
* Arduino_BMI270_BMM150.h
* ReefwingAHRS.h

## Démarrage
SANS ARDUINO :
* compiler puis exécuter HandTrackingExecution.c

AVEC ARDUINO :
* faire le [montage](Others/circuit.odg)
* upload [code_arduino](Code/Arduino/code_arduino/code_arduino.ino)
* lancer le main_arduino.py

## Utilisation
* ![Tableau](https://github.com/Yotoon2/Projet-CMI-1-2025/blob/main/Emojis/Tableau.png) : change entre le mode dessin et le mode laser (Première activation : mode dessin)
* ![Thumb Left](https://github.com/Yotoon2/Projet-CMI-1-2025/blob/main/Emojis/Thumb_Left.png) : Revenir à la diapositive précédente
* ![Thumb Right](https://github.com/Yotoon2/Projet-CMI-1-2025/blob/main/Emojis/Thumb_Right.png) : Aller à la diapositive suivante
* ![Pince](https://github.com/Yotoon2/Projet-CMI-1-2025/blob/main/Emojis/pince.png) : Dessine/ déplace le pointeur laser
* ![Middle Finger](https://github.com/Yotoon2/Projet-CMI-1-2025/blob/main/Emojis/middle_finger.png) : Ferme le diaporama et arrête le programme
  
### Auteurs
* [@nexy-us](https://github.com/nexy-us)
* [@Yotoon2](https://github.com/Yotoon2)
* [@hind270](https://github.com/hind270)

### License

MIT
