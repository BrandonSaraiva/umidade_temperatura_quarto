#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>

#define DHTPIN 2  // Pino onde o sensor está conectado
#define DHTTYPE DHT22  // Modelo do sensor (DHT22)

DHT_Unified dht(DHTPIN, DHTTYPE);
unsigned long previousMillis = 0;  // Variável para armazenar o tempo da última leitura
const long interval = 3600000;  // Intervalo de 1 hora em milissegundos

void setup() {
  Serial.begin(9600);  // Inicializa a comunicação serial
  dht.begin();  // Inicializa o sensor DHT
  sensor_t sensor;
  dht.temperature().getSensor(&sensor);  // Obtém informações do sensor
  dht.humidity().getSensor(&sensor);

  // Inicializa previousMillis para garantir a leitura imediata dos dados
  previousMillis = millis() - interval;
}

void loop() {
  unsigned long currentMillis = millis();  // Obtém o tempo atual

  // Verifica se passou 1 hora desde a última leitura
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;  // Atualiza o tempo da última leitura

    sensors_event_t event;

    // Leitura da temperatura
    dht.temperature().getEvent(&event);
    Serial.print("Temperatura: ");
    Serial.print(event.temperature);
    Serial.println(" *C");

    // Leitura da umidade
    dht.humidity().getEvent(&event);
    Serial.print("Umidade: ");
    Serial.print(event.relative_humidity);
    Serial.println(" %");
  }
}
