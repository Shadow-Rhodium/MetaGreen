#include <IRremote.h>
#include <SimpleDHT.h>


int MO = A0;
int CO2 = A1;
int light = A2;
int DHT = 3;
int LDR = 7;
int ir = 11;

SimpleDHT11 dht11(10);

byte temp = 0;   
byte hmid = 0;

int s = 0;
int l = 0;
int D = 0;
int w = 0;
int i = 0;
int m = 0;

void setup() {
  // put your setup code here, to run once:
pinMode(MO, INPUT);
pinMode(light, INPUT);
pinMode(CO2, INPUT);
pinMode(ir, INPUT);
pinMode(LDR, INPUT);

Serial.begin(9600);
IrReceiver.begin(ir, ENABLE_LED_FEEDBACK);

}

void loop() {
  // put your main code here, to run repeatedly:


  s = analogRead(CO2);
  l = analogRead(light);
  m = analogRead(m);
  w = digitalRead(LDR);
  D = dht11.read(&temp, &hmid,NULL);


int lst[] = {s,l,temp,hmid,w,m};

for (byte i = 0; i < 6; i = i + 1) {
  Serial.print(lst[i]);
  Serial.print(" ");
}

 if (IrReceiver.decode())
   {
      unsigned long keycode = IrReceiver.decodedIRData.command;
      Serial.print(keycode, HEX);
      if ((IrReceiver.decodedIRData.flags & IRDATA_FLAGS_IS_REPEAT)) // ignore repeat code
      {
         IrReceiver.resume();
         return;
      }
      IrReceiver.resume();
  
}

Serial.println();
  delay(2000);





}
