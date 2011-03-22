#include "WProgram.h"
#include "EventParser.h"

EventParser::EventParser() {
    this->state = STATE_WAITING;
    this->total = 0;
    this->count = 0;
  
    this->handlers_last_index = 0;
    
    this->MAX_BUFFER = 128;
    this->char_buffer = (char *) malloc(sizeof(char)*this->MAX_BUFFER);
    this->char_buffer_offset = 0;
    
    this->temp_event = Event();
}

EventParser::~EventParser() {
  free(this->char_buffer);
}

boolean EventParser::register_handler(char *type, eventhandler handler, int *type_int) {
  if (this->handlers_last_index < MAX_HANDLERS) {
    this->handlers[this->handlers_last_index] = handler;
    this->handlers_type_map[this->handlers_last_index] = type;
    
    *type_int = this->handlers_last_index;
    this->handlers_last_index += 1;
    
    return true;
  }

  return false;
}


EventParser& EventParser::concat(char c) {   
  switch(this->state) {
    case STATE_WAITING:
      if (c == TOKEN_START) {
        this->push_buffer(c);
        this->state = STATE_START;
      }
      break;
    
    case STATE_START:
      if (c == TOKEN_SEP) {
        this->clear_buffer();
        this->state = STATE_WAITING;
      }
      else if (c == TOKEN_TOTAL_SEP) {     
        this->push_buffer('\0');
        if (!strcmp(this->char_buffer, "total"))
          this->state = STATE_TOTAL;
        else
          this->state = STATE_WAITING;

        this->clear_buffer();        
      }
      else {
        this->push_buffer(c);
      }      
      break;
        
    case STATE_TOTAL:
      if (c == TOKEN_SEP) {
        this->push_buffer('\0');
        this->total = atoi(this->char_buffer);    
        
        if (this->total == 0)
          this->state = STATE_END;
        else 
          this->state = STATE_EVENT_TYPE;        
  
        this->clear_buffer();          
      }  
      else {
        this->push_buffer(c);
      }
     
      break;   
      
    case STATE_EVENT_TYPE:
      if (c == TOKEN_SEP) {
        this->clear_buffer();
        this->state = STATE_WAITING;
      }
      else if (c == TOKEN_EVENT_SEP) {
        this->push_buffer('\0');
        this->temp_event.set_type(this->char_buffer);
        this->clear_buffer();
        this->state = STATE_EVENT_DATA;
      } 
      else if (c != '\r') {
         this->push_buffer(c);
      }
      break;
      
    case STATE_EVENT_DATA:
      if (c == TOKEN_SEP) {       
        this->push_buffer('\0');        
        this->temp_event.set_data(this->char_buffer);
        this->clear_buffer();
        this->count += 1;
        
        eventhandler handler = this->lookup_handler(this->temp_event.type);
        if (handler != NULL) {
          Event event = Event();
          event.set_type(this->temp_event.type);
          event.set_data(this->temp_event.data);
          
          handler(&event);        
        }
        
        if (this->count == this->total)
          this->state = STATE_END;
        else
          this->state = STATE_EVENT_TYPE;
      }
      else {
         this->push_buffer(c);
      }
      break;
    
    case STATE_END:
      break;
      
    default:
      break;
  }  
  return *this;
}

EventParser::eventhandler EventParser::lookup_handler(char *type) {
  // TODO: write a hashtable library
  for (int i=0; i<MAX_HANDLERS; i++) {
    if (!strcmp(this->handlers_type_map[i], type))
      return this->handlers[i];
  }
  
  return NULL;
}

void EventParser::eos() {
  this->concat('\n');
}

void EventParser::reset() {
  this->clear_buffer();
  this->state = STATE_WAITING;
  this->temp_event.set_type("");
  this->temp_event.set_data("");  
}

void EventParser::clear_buffer() {
  this->char_buffer_offset = 0;
  this->char_buffer[0] = '\0';
}

boolean EventParser::push_buffer(char c) {
  // Leave room for a null character
  if (this->char_buffer_offset == this->MAX_BUFFER-2) {
    this->char_buffer[this->char_buffer_offset] = '\0';
    this->char_buffer_offset += 1;
    return false;
  }
  else if (this->char_buffer_offset == this->MAX_BUFFER-1) {
    return false;
  }  
  else {  
    this->char_buffer[this->char_buffer_offset] = c;
    this->char_buffer_offset += 1;
    return true;
  }
}
