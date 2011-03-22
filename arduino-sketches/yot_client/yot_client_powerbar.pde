#include <Ethernet.h>
#include <SPI.h>
#include <Streaming.h>
#include "EventParser.h"

#include <Temperature.h>
#include <Powerbar.h>

#define YOT_CLIENT_DEBUG            1
#define YOT_CLIENT_DEVELOPMENT      1

#if YOT_CLIENT_DEVELOPMENT
byte client_mac[] = {0x90, 0xA2, 0xDA, 0x00, 0x36, 0xFC};
byte client_ip[] = {192, 168, 1, 150};
char client_name[] = "ddimit";

char yot_poll[] = "/poll";
char yot_post[] = "/post";

char yot_host[] = "";
byte yot_ip[] = {192, 168, 1, 105};
short int yot_port = 80;
#else
byte client_mac[] = {0x90, 0xA2, 0xDA, 0x00, 0x36, 0xFC};
byte client_ip[] = {192, 168, 1, 150};
char client_name[] = "ddimit";

char yot_poll[] = "/yot.fcgi/poll";
char yot_post[] = "/yot.fcgi/post";

char yot_host[] = "yot.h55k.com";
byte yot_ip[] = {67, 205, 91, 197};
short int yot_port = 80;
#endif

Client client = Client(yot_ip, yot_port);

int post_delay = 15000;
int poll_delay = 5000;

enum state {POST, POLL, NONE};
enum state locked = NONE;

long last_post_time = 0;
long last_poll_time = 0;
boolean last_connected = false;
  
// Remove this
Temperature temp(2);
Powerbar powerbar(8);

// No time to test for memory leaks (thanks C), so declare only once
EventParser parser = EventParser();

// Event handler for POWERBAR events
void powerbar_handler(Event *event) {
  #if YOT_CLIENT_DEBUG
  Serial << "[received event] " << (*event).type << ":" << (*event).data << "\n";
  #endif 

  int data = atoi((*event).data);  
  if (data == 0)
    powerbar.off();
  else if (data == 1)
    powerbar.on();
}

void poll(Client *client, char url[]) {
  (*client) << "GET " << url <<"/" << client_name << " HTTP/1.1\r\n"
            << "Host: " << yot_host << "\r\n"  
            << "Connection: close\r\n"
            << "\r\n";
}

void post(Client *client, char url[], char data[], int data_length) {
  (*client)  << "POST " << url << " HTTP/1.1\r\n"
             << "Host: " << yot_host << "\r\n" 
             << "Content-Type: application/x-www-form-urlencoded\r\n"             
             << "Content-Length: " << data_length << "\r\n" 
             << "Connection: close\r\n"
             << "\r\n"
             << data;
}

// Called when the results of a post need to be read
void try_read_post(Client *client) {
  (*client).flush();
}

// Called when the results of a poll need to be read
void try_read_poll(Client *client) {          
  while ((*client).connected()) {
    if ((*client).available()) 
      parser.concat((*client).read());            
  }
  parser.eos();      
  parser.reset();
}

// Try to stop the client
boolean try_stop_client(Client *client, boolean *last_connected) {
  if (!(*client).connected() && *last_connected) {
    #if YOT_CLIENT_DEBUG
    Serial << "[net] disconnecting" << "\n";
    #endif
    (*client).stop();
    return true;
  }      
  return false;
}  

// Try to poll
void try_poll(Client *client) {
  if ((*client).connect()) {
    #if YOT_CLIENT_DEBUG
    Serial << "[net] polling" << "\n";
    #endif
    
    poll(client, yot_poll);
  }
  else {
    #if YOT_CLIENT_DEBUG
    Serial << "[net] polling connection failed" << "\n";
    #endif
  }
  
  last_poll_time = millis();
}

// Try to post
void try_post(Client *client) {
  if ((*client).connect()) {
    #if YOT_CLIENT_DEBUG
    Serial << "[net] posting" << "\n";
    #endif
        
    // TODO: remove hardcoding of temperature
    double temp_reading;
    temp.get_temperature(&temp_reading);
    
    String buffer = "event={\"type\":\"TEMPERATURE\",\"sender\":\"ddimit\",\"data\":\"";
    buffer += String((long) temp_reading, DEC);
    buffer += String("\"} ");
    
    char charbuffer[buffer.length()];
    buffer.toCharArray(charbuffer, buffer.length());
    post(client, yot_post, charbuffer, buffer.length()-1);        
  }
  else {
    #if YOT_CLIENT_DEBUG
    Serial << "[net] posting connection failed" << "\n";
    #endif
  }
  
  last_post_time = millis();
}

void setup() {
    int powerbar_event_type_int = 0;
    parser.register_handler("POWERBAR", &powerbar_handler, &powerbar_event_type_int);

    Ethernet.begin(client_mac, client_ip);
   
    #if YOT_CLIENT_DEBUG
    Serial.begin(9600);
    Serial << "[serial] initialized" << "\n";
    #endif
    
    delay(1000);
}

void loop() {
  switch(locked) {
    case POLL:
      try_read_poll(&client);
      break;
    case POST:
      try_read_post(&client);
      break;
    default:
      break;
  }    
  
  try_stop_client(&client, &last_connected);

  if(!client.connected() && (millis() - last_poll_time > poll_delay)) {
    locked = POLL;   
    try_poll(&client);
  }   

  else if(!client.connected() && (millis() - last_post_time > post_delay)) {    
    locked = POST;
    try_post(&client);   
  }

  last_connected = client.connected();         
}      
