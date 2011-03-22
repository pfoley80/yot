#include <Ethernet.h>
#include <SPI.h>
#include <Streaming.h>

#include <Temperature.h>
#include <Powerbar.h>

#define DEBUG            1
#define POLL_BUFFER_SIZE 1024

#if DEBUG
byte client_mac[] = {0x90, 0xA2, 0xDA, 0x00, 0x36, 0xFC};
byte client_ip[] = {192, 168, 1, 150};
byte client_gateway[] = {192,168,1,1};
char client_name[] = "ddimit";

char yot_poll[] = "/poll";
char yot_post[] = "/post";

char yot_host[] = "";
byte yot_ip[] = {192, 168, 1, 201};
short int yot_port = 80;
#else
byte client_mac[] = {0x90, 0xA2, 0xDA, 0x00, 0x36, 0xFC};
byte client_ip[] = {192, 168, 1, 150};
byte client_gateway[] = {192,168,1,1};
char client_name[] = "ddimit";

char yot_poll[] = "/yot.fcgi/poll";
char yot_post[] = "/yot.fcgi/post";

char yot_host[] = "yot.h55k.com";
byte yot_ip[] = {67, 205, 91, 197};
short int yot_port = 80;
#endif

Client client(yot_ip, yot_port);

int io_delay = 15000;
long last_connection_time = 0;
boolean last_connected = false;
  
// Remove this
Temperature temp(2);

void try_post(Client *client) {
  if ((*client).connect()) {
    #if DEBUG
    Serial.println("Posting");
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
    
    last_connection_time = millis();
  }
  else {
    #if DEBUG
    Serial.println("Connection failed");
    #endif
  }
}

void poll(Client *client, char url[], char buffer[]) {
  (*client) << "GET " << url << "HTTP/1.1\r\n"
            << "Host: " << yot_host;
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

void setup() {
    Ethernet.begin(client_mac, client_ip, client_gateway);
   
    #if DEBUG
    Serial.begin(9600);
    #endif
    
    delay(1000);
}

void loop() {
  if (client.available()) {
    char c = client.read();
    Serial.print(c);
  }

  if (!client.connected() && last_connected) {
    Serial.println();
    Serial.println("disconnecting.");
    client.stop();
  }

  if(!client.connected() && (millis() - last_connection_time > io_delay)) {
    try_post(&client);
  }
  
  last_connected = client.connected();
}
