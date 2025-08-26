#include <LiquidCrystal.h>

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(4,OUTPUT);

}

char c;
void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available())
  {
    c = Serial.read();
    digitalWrite(4,HIGH);
    }
  delay(1000);
  digitalWrite(4,LOW);

}
