//Аддон для Arduino IDE для работы с RuFA Connect


#include "RuFAConnect.h"

RuFAConnect::RuFAConnect(HardwareSerial &serial) {
  _serial = &serial;
}

void RuFAConnect::begin(long baudRate) {
  _serial->begin(baudRate);
}

void RuFAConnect::sendData(const char* data) {
  _serial->println(data);
}

String RuFAConnect::receiveData() {
  String data = "";
  while (_serial->available()) {
    data += (char)_serial->read();
  }
  return data;
}
