#include <WiFiNINA.h>
#include <PubSubClient.h>

// Wi-Fi 설정
const char* ssid = "ECSL-2.4GHz";
const char* password = "ecsl13204";

// MQTT 브로커 설정
const char* mqtt_server = "192.168.0.13";
const int mqtt_port = 1883;
const char* topic = "temp";

WiFiClient wifiClient;
PubSubClient client(wifiClient);

void setup() {
  Serial.begin(9600);
  connectWiFi();
  client.setServer(mqtt_server, mqtt_port);
}
void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  static unsigned long lastMsg = 0;
  if (millis() - lastMsg > 5000) {
    lastMsg = millis();
    
    // 임시 온도 값 생성 (실제 센서 연결 시 수정 필요)
    float temp = random(20, 30);
    char msg[50];
    snprintf(msg, 50, "%.2f", temp);
    
    client.publish(topic, msg);
    Serial.print("Published: ");
    Serial.println(msg);
  }
}

void connectWiFi() {
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print("Connecting to ");
    Serial.println(ssid);
    WiFi.begin(ssid, password);
    delay(5000);
  }
  Serial.println("WiFi connected");
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("MQTT connecting...");
    if (client.connect("ArduinoNano")) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" retry in 5s");
      delay(5000);
    }
  }
}