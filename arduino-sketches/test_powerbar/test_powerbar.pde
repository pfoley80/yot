#include <Powerbar.h>

#define BAUDRATE 9600

int incoming_byte = -1;
int buffer_pos = 0;
boolean t = false;

int pin = 8;

Powerbar powerbar(pin);

void setup() {
  Serial.begin(BAUDRATE);
}

void loop() {
  if (Serial.available() > 0) {
    incoming_byte = Serial.read();
  
    if (incoming_byte != -1) {
      t = boolean(incoming_byte - 48);
      Serial.print("Power ");
      Serial.println(t ? 1 : 0);
      powerbar.toggle(t);
      Serial.print("Result: ");
      Serial.println(powerbar.state() ? 1 : 0);
    }
  }
}
