#define O0 11
#define O1 10
#define O2 9
#define O3 6
#define O4 5
int t=80;

void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
pinMode(O1,OUTPUT);
pinMode(O2,OUTPUT);

}

void loop() {

  digitalWrite(O1,HIGH);
  delay(t/2);
  digitalWrite(O2,HIGH);
  delay(t/2);
  digitalWrite(O1,LOW);
  delay(t/2);
  digitalWrite(O2,LOW);
  delay(t/2);
  
   if (Serial.available()>0) 
   {
        t = (Serial.readString()).toInt();
      delay(100);
   }

}
