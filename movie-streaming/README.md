## Minimal OTT Platform with Apache Kafka Streaming
This is a minimal implementation of an OTT Plaform with UI highly inspired from Amazon Prime Video. This application uses Apache Kafka Topics to read the video.

## Steps to run this application 
1. Create a .bat file in your Kafka folder (Windows)
```
@echo off
start cmd /k "E:\kafka\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties"
start cmd /k "E:\kafka\bin\windows\kafka-server-start.bat .\config\server.properties"
```
2. Run the bat file  
      This will keep the Kafka Zookeeper and the Kafka Server Up.
3. Loads data to the Kafka Topic  
`python manage.py producer "path of video file" `
4. Run the server  
`python manage.py runserver`
5. Go to `http://localhost:8000` in your browser