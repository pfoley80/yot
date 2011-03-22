#include "WProgram.h"
#include "Event.h"

Event::Event() {
  this->type = NULL;
  this->data = NULL;
}

Event::Event(char *type) {    
  this->data = NULL;
  this->set_type(type);
}

Event::~Event() {
  if (this->type != NULL)
    free(this->type);

  if (this->data != NULL)
    free(this->data);
}


void Event::set_type(char *type) {
  if (this->type != NULL)
    free(this->type);
  
  int len = strlen(type) + 1;
  this->type = (char *) malloc(sizeof(char)*len);
  strcpy(this->type, type);
}

void Event::set_data(char *data) {
  if (this->data != NULL)
    free(this->data);
  
  int len = strlen(data) + 1;
  this->data = (char *) malloc(sizeof(char)*len);
  strcpy(this->data, data);
}

