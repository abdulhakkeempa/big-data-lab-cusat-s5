## Minimal OTT Platform with Apache Kafka Streaming
This is a minimal implementation of an OTT Plaform with UI highly inspired from Amazon Prime Video. This application uses Apache Kafka Topics to read the video.

## Steps to run this application 
1. Loads data to the Kafka Topic  
`python manage.py producer "path of video file" `
2. Run the server  
`python manage.py runserver`
3. Go to `http://localhost:8000` in your browser