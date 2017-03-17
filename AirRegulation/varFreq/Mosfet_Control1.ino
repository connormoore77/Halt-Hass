#define O0 11
#define O1 10
#define O2 9
#define O3 6
#define O4 5
int deltaT=80;

void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
pinMode(O1,OUTPUT);
pinMode(O2,OUTPUT);
pinMode(03,OUTPUT);

}

void loop() {

  digitalWrite(O1,HIGH);
  delay(deltaT/6);
  digitalWrite(O1,LOW);
  digitalWrite(02,HIGH);
  delay(deltaT/6);
  digitalWrite(02,LOW);
  digitalWrite(03,HIGH);
  delay(deltaT/6);
  digitalWrite(O3,LOW);
  delay(deltaT/6);
  
   if (Serial.available()>0) 
   {
        deltaT = (Serial.readString()).toInt();
      delay(100);
   }

}
