
## rp2040으로 랜덤한 값(온도 값)을 만들어 mqtt를 통해 라즈베리파이4(debian bullseye 64bit)에서 
## 값을 받아 mysql에서 temperature_db에 값을 저장하고 
## influxdb(http://localhost:8086)를 이용하여 온도값 그래프를 그려서 브라우저에 띄우는 과정

### influxdb에서 그린 그래프 
![Image](https://github.com/user-attachments/assets/8254f804-5f20-4eef-810c-f63720d306f1)

### influxdb에 저장된 값 
![Image](https://github.com/user-attachments/assets/a7f6acdf-8189-42f6-b8fb-419127fb94ed)

### VCS DATEBASE를 통해 MYSQL에 저장된 값 확인 
![Image](https://github.com/user-attachments/assets/efe226c3-628a-4a57-8ff0-749ca47b9918)

### rp2040에서 mqtt로 전송된 값
![Image](https://github.com/user-attachments/assets/1e7fe664-85a2-459d-9117-183d7080da09)
