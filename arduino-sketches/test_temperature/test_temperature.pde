#include <Temperature.h>
#include <Streaming.h>

// Event stuff
void send_event(char **name, double *data);

int pin = 2;
char event_name[] = "push_temp";

Temperature temp(pin);
double temp_reading;

void setup() {
  Serial.begin(9600);
}

void loop() {
  temp.get_temperature(&temp_reading);
  temp_reading -= 3; // Fix weird reading
  
  send_event(event_name, &temp_reading);
  delay(1000);        
}

void send_event(char *name, double *data) {
  Serial << "event:" << name << ":" << *data << "\r\n";
} 
