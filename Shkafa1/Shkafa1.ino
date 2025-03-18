#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>
#include <UniversalTelegramBot.h>
#include <Servo.h>
#include <WiFiUdp.h>  // Подключаем библиотеку для работы с UDP

// Wifi network station credentials
#define WIFI_SSID "WIFI_SSID"
#define WIFI_PASSWORD "WIFI_PASSWORD"

// Telegram BOT Token (Get from Botfather)
#define BOT_TOKEN "Telegram BOT Token"

const unsigned long BOT_MTBS = 1000; // mean time between scan messages

X509List cert(TELEGRAM_CERTIFICATE_ROOT);
WiFiClientSecure secured_client;
UniversalTelegramBot bot(BOT_TOKEN, secured_client);
unsigned long bot_lasttime; // last time messages' scan has been done

const int ledPin = LED_BUILTIN;
int ledStatus = 0;

Servo myServo;
const int servoPin = D3;
int servoStatus = 0;

// UDP параметры
WiFiUDP udp;
const char* udpAddress = "192.168.1.100"; // Адрес получателя (например, IP вашего компьютера или сервера)
const int udpPort = 12345; // Порт для UDP отправки

unsigned long lastJsonSendTime = 0; // Время последней отправки JSON

// Функция для отправки JSON пакета
void sendJsonStatus() {
  // Создаём JSON-объект
  StaticJsonDocument<200> doc;
  
  // Добавляем в объект информацию о состоянии сервопривода и светодиода
  doc["ledStatus"] = ledStatus;
  doc["servoStatus"] = servoStatus;
  
  // Преобразуем JSON-объект в строку
  String jsonString;
  serializeJson(doc, jsonString);
  
  // Отправляем JSON-строку через UDP
  udp.beginPacket(udpAddress, udpPort);
  udp.write(jsonString.c_str());
  udp.endPacket();
}

void handleNewMessages(int numNewMessages)
{
  Serial.print("handleNewMessages ");
  Serial.println(numNewMessages);

  for (int i = 0; i < numNewMessages; i++)
  {
    String chat_id = bot.messages[i].chat_id;
    String text = bot.messages[i].text;

    String from_name = bot.messages[i].from_name;
    if (from_name == "")
      from_name = "Guest";

    if (text == "/on")
    {
      digitalWrite(ledPin, LOW); // turn the LED on (HIGH is the voltage level)
      ledStatus = 1;
      myServo.write(90);  // Поворачиваем серво на 90 градусов
      servoStatus = 1;    // Серво в положении "включено"
      bot.sendMessage(chat_id, "LED and Servo are ON", "");
    }

    if (text == "/off")
    {
      ledStatus = 0;
      digitalWrite(ledPin, HIGH); // turn the LED off (LOW is the voltage level)
      myServo.write(0);  // Поворачиваем серво на 0 градусов
      servoStatus = 0;    // Серво в положении "выключено"
      bot.sendMessage(chat_id, "LED and Servo are OFF", "");
    }

    if (text == "/status")
    {
      if (ledStatus)
      {
        bot.sendMessage(chat_id, "LED is ON", "");
      }
      else
      {
        bot.sendMessage(chat_id, "LED is OFF", "");
      }
      
      if (servoStatus == 90)
      {
        bot.sendMessage(chat_id, "Servo is ON (90 degrees)", "");
      }
      else
      {
        bot.sendMessage(chat_id, "Servo is OFF (0 degrees)", "");
      }
    }

    if (text == "/start")
    {
      String welcome = "Welcome to Universal Arduino Telegram Bot library, " + from_name + ".\n";
      welcome += "This is Flash LED and Servo control Bot example.\n\n";
      welcome += "/on : to switch the Led and Servo ON\n";
      welcome += "/off : to switch the Led and Servo OFF\n";
      welcome += "/status : Returns current status of LED and Servo\n";
      bot.sendMessage(chat_id, welcome, "Markdown");
    }
  }
}

void setup()
{
  Serial.begin(115200);
  Serial.println();

  myServo.attach(servoPin);

  pinMode(ledPin, OUTPUT); // initialize digital ledPin as an output.
  delay(10);
  digitalWrite(ledPin, HIGH); // initialize pin as off (active LOW)

  // attempt to connect to Wifi network:
  configTime(0, 0, "pool.ntp.org");      // get UTC time via NTP
  secured_client.setTrustAnchors(&cert); // Add root certificate for api.telegram.org
  Serial.print("Connecting to Wifi SSID ");
  Serial.print(WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(500);
  }
  Serial.print("\nWiFi connected. IP address: ");
  Serial.println(WiFi.localIP());

  // Check NTP/Time, usually it is instantaneous and you can delete the code below.
  Serial.print("Retrieving time: ");
  time_t now = time(nullptr);
  while (now < 24 * 3600)
  {
    Serial.print("...");
    delay(100);
    now = time(nullptr);
  }
  Serial.println(now);

  // Инициализация UDP
  udp.begin(udpPort);
}

void loop()
{
  if (millis() - bot_lasttime > BOT_MTBS)
  {
    int numNewMessages = bot.getUpdates(bot.last_message_received + 1);

    while (numNewMessages)
    {
      Serial.println("got response");
      handleNewMessages(numNewMessages);
      numNewMessages = bot.getUpdates(bot.last_message_received + 1);
    }

    bot_lasttime = millis();
  }

  // Отправляем JSON каждые 2 секунды
  if (millis() - lastJsonSendTime >= 2000) // 2 секунды
  {
    sendJsonStatus(); // Отправляем JSON
    lastJsonSendTime = millis(); // Обновляем время последней отправки
  }
}
