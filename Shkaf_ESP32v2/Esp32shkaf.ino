#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <ESPmDNS.h>
#include <NetworkUdp.h>
#include <ArduinoOTA.h>

#include <UniversalTelegramBot.h>
#include <ESP32Servo.h>  // Используем библиотеку ESP32Servo для работы с сервоприводом

#define WIFI_SSID "WIFI_SSID"
#define WIFI_PASSWORD "WIFI_PASSWORD"

// Telegram BOT Token (получить у @BotFather)
#define BOT_TOKEN "BOT_TOKEN"

const unsigned long BOT_MTBS = 1000; // интервал между запросами боту

WiFiClientSecure secured_client;
UniversalTelegramBot bot(BOT_TOKEN, secured_client);
unsigned long bot_lasttime;

Servo myServo;
const int servoPin = 33;
int servoStatus = 0;

// whitelist
const String WHITELIST[] = {
  "2112312344", //your id
  "2174567854",

};
const int WHITELIST_SIZE = sizeof(WHITELIST) / sizeof(WHITELIST[0]);

// 🔐  Access verification
bool isAuthorized(String chat_id) {
  for (int i = 0; i < WHITELIST_SIZE; i++) {
    if (WHITELIST[i] == chat_id) {
      return true;
    }
  }
  return false;
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
    if (from_name == "") from_name = "Guest";

    // 🔐 Проверка, есть ли доступ
    if (!isAuthorized(chat_id)) {
      Serial.println("🔒 Неавторизованная попытка доступа от chat_id: " + chat_id);
      bot.sendMessage(chat_id, "❌ У вас нет доступа к этому боту.", "");
      continue;
    }

    // ✅ Разрешённые команды
    if (text == "/open") {
      myServo.write(90);
      servoStatus = myServo.read();
      bot.sendMessage(chat_id, "Открыто", "");
    }
    else if (text == "/close") {
      myServo.write(0);
      servoStatus = myServo.read();
      bot.sendMessage(chat_id, "Закрыто", "");
    }
    else if (text == "/status") {
      bot.sendMessage(chat_id, servoStatus > 0 ? "Открыто" : "Закрыто", "");
    }
    else if (text == "/start") {
      String welcome = "Привет, " + from_name + "!\n";
      welcome += "Я бот для управления сервоприводом.\n\n";
      welcome += "/open – открыть\n";
      welcome += "/close – закрыть\n";
      welcome += "/status – текущий статус\n";
      bot.sendMessage(chat_id, welcome, "Markdown");
    }
  }
}

void setup() {
  Serial.begin(115200);
  Serial.println("Booting");
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  while (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.println("Connection Failed! Rebooting...");
    delay(5000);
    ESP.restart();
  }

  delay(10);
  myServo.attach(servoPin);
  myServo.write(0);
  servoStatus = 0;

  Serial.print("Connecting to Wi-Fi SSID ");
  Serial.println(WIFI_SSID);
  secured_client.setCACert(TELEGRAM_CERTIFICATE_ROOT);

  ArduinoOTA
    .onStart([]() {
      String type = ArduinoOTA.getCommand() == U_FLASH ? "sketch" : "filesystem";
      Serial.println("Start updating " + type);
    })
    .onEnd([]() {
      Serial.println("\nEnd");
    })
    .onProgress([](unsigned int progress, unsigned int total) {
      Serial.printf("Progress: %u%%\r", (progress / (total / 100)));
    })
    .onError([](ota_error_t error) {
      Serial.printf("Error[%u]: ", error);
      if (error == OTA_AUTH_ERROR) Serial.println("Auth Failed");
      else if (error == OTA_BEGIN_ERROR) Serial.println("Begin Failed");
      else if (error == OTA_CONNECT_ERROR) Serial.println("Connect Failed");
      else if (error == OTA_RECEIVE_ERROR) Serial.println("Receive Failed");
      else if (error == OTA_END_ERROR) Serial.println("End Failed");
    });

  ArduinoOTA.begin();

  Serial.println("Готово к работе");
  Serial.print("IP адрес: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  ArduinoOTA.handle();

  if (millis() - bot_lasttime > BOT_MTBS) {
    int numNewMessages = bot.getUpdates(bot.last_message_received + 1);
    while (numNewMessages) {
      Serial.println("Новое сообщение");
      handleNewMessages(numNewMessages);
      numNewMessages = bot.getUpdates(bot.last_message_received + 1);
    }
    bot_lasttime = millis();
  }
}
