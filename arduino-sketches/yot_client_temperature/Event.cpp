#include "WProgram.h"
#include "Event.h"

Event::Event() {
  // Init the queue
  
  // Initialize our array lengths
  _event_types_count = 0;
  _handlers_count = 0;
  
  register_type(Event::REGISTER_EVENT_TYPE);
  register_type(Event::UNREGISTER_EVENT_TYPE);
}

boolean Event::register_type(int type) {
  if (_event_types_count == MAX_EVENT_TYPES)
    return false;
  
  _event_types[_event_types_count] = type;
  _event_types_count += 1;
  return true;
}

boolean Event::unregister_type(int type) {
  return false; // TODO
}

boolean Event::bind_handler(int type, event_handler *handler) {
    
}

boolean Event::unbind_handler(int type, event_handler *handler) {
}

boolean Event::push_event(event *evt) {
}

boolean Event::pop_event(event *evt) {
}

