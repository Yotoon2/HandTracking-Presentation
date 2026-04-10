const int pinPouce = A0;
const int pinIndex = A6;
const int pinMajeur = A5;

int valeurPouce = 0;
int valeurIndex = 0;
int valeurMajeur = 0;

int positionPouce = 0;
int positionIndex = 0;
int positionMajeur = 0;

// CALIBRATIONS
const int seuilBas = 100;  
const int seuilHaut = 230;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int lecturePouce = analogRead(pinPouce);
  int lectureIndex = analogRead(pinIndex);
  int lectureMajeur = analogRead(pinMajeur);

  valeurPouce = (valeurPouce + lecturePouce) / 2;
  valeurIndex = (valeurIndex + lectureIndex) / 2;
  valeurMajeur = (valeurMajeur + lectureMajeur) / 2;

  // Pouce

  if(valeurPouce > seuilHaut){ // Pas plié
    positionPouce = 0;
  }
  else if(valeurPouce > seuilBas){ // Semi-plié
    positionPouce = 1;
  }
  else{ // Plié
    positionPouce = 2;
  }

  if(valeurIndex > seuilHaut){ // Pas plié
    positionIndex = 0;
  }
  else if(valeurIndex > seuilBas){ // Semi-plié
    positionIndex = 1;
  }
  else{ // Plié
    positionIndex = 2;
  }
  // Majeur
  
  if(valeurMajeur > seuilHaut){ // Pas plié
    positionMajeur = 0;
  }
  else if(valeurMajeur > seuilBas){ // Semi-plié
    positionMajeur = 1;
  }
  else{ // Plié
    positionMajeur = 2;
  }
  /*Serial.print(positionPouce);
  Serial.print(positionIndex);
  Serial.println(positionMajeur);*/
  
  //Serial.print("Valeur "); Serial.print(valeur);
  /*erial.print("Position Pouce : ");
  switch(positionPouce) {
    case 0: Serial.println("Ouvert"); break;
    case 1: Serial.println("Semi-plié"); break;
    case 2: Serial.println("Fermé"); break;
  }*/

  
  Serial.print("{\"flex\":["); Serial.print(valeurPouce); Serial.print(","); Serial.print(valeurIndex); Serial.print(","); Serial.print(valeurMajeur); Serial.println("]}");
  
  /*Serial.print("Position Index : ");
  switch(positionIndex) {
    case 0: Serial.println("Ouvert"); break;
    case 1: Serial.println("Semi-plié"); break;
    case 2: Serial.println("Fermé"); break;
  }
  
  Serial.print("Position Majeur : ");
  switch(positionMajeur) {
    case 0: Serial.println("Ouvert"); break;
    case 1: Serial.println("Semi-plié"); break;
    case 2: Serial.println("Fermé"); break;
  }
  Serial.println(valeurPouce);
  Serial.println(valeurMajeur);*/
    /*
  if ((positionPouce == 2) && (positionIndex == 2) && (positionMajeur == 2)){
    Serial.print("Poing fermé !");
  }

  if ((positionPouce == 1) && (positionIndex == 1) && (positionMajeur == 0)){
    Serial.print("Pince");
  }
  */

  delay(200);
}