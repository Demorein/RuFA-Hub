//Аддон для Arduino IDE для работы с RuFA Connect


#include "RuFAConnect.h"

// Конструктор
RuFAConnect::RuFAConnect(HardwareSerial &serial) {
  _serial = &serial;
}

// Инициализация порта
void RuFAConnect::begin(long baudRate) {
  _serial->begin(baudRate);
}

// Отправка данных
void RuFAConnect::sendData(const char* data) {
  _serial->println(data);  // Отправляем строку через последовательный порт
}

// Получение данных (если нужно)
String RuFAConnect::receiveData() {
  String data = "";
  while (_serial->available()) {
    data += (char)_serial->read();
  }
  return data;
}
