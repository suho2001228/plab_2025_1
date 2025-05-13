import mysql.connector
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS  # 추가

# InfluxDB 설정
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "DxfRoED5wabPSttn5AkfZkMGsPe9HiXBF-pIsUPFW7ri0eylOTWDJU2dClsMa9oQOnt84BbaJDxQjTQz5_rfDQ=="
INFLUXDB_ORG = "kunsan"
INFLUXDB_BUCKET = "jsh_db"

# MQTT 브로커 설정
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "temp"

# InfluxDB 클라이언트 생성
influx_client = InfluxDBClient(
    url=INFLUXDB_URL,
    token=INFLUXDB_TOKEN,
    org=INFLUXDB_ORG
)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)  # 반드시 이렇게!

# MySQL 설정
MYSQL_HOST = "localhost"
MYSQL_USER = "jsh"
MYSQL_PASSWORD = "97531"  # MySQL 비밀번호 입력
MYSQL_DATABASE = "temperature_db"

# MySQL 연결
def connect_mysql():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

# 온도 데이터를 MySQL에 저장하는 함수
def save_to_mysql(temp_value):
    conn = connect_mysql()
    cursor = conn.cursor()
    
    # 테이블이 없다면 생성
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS temperature_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        temperature FLOAT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # 데이터 삽입
    cursor.execute("INSERT INTO temperature_data (temperature) VALUES (%s)", (temp_value,))
    conn.commit()
    cursor.close()
    conn.close()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    temp_value = float(msg.payload.decode())
    print(f"Received temp: {temp_value}")

    # InfluxDB에 저장
    point = Point("temperature").field("value", temp_value)
    write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)

    # MySQL에 저장
    save_to_mysql(temp_value)

# MQTT 클라이언트 설정
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# MQTT 브로커에 연결
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

# MQTT 메시지 루프 시작
mqtt_client.loop_forever()
