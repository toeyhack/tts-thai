-copy file to folder Ex. /tts-api
-cd tts-api
-sudo docker build -t thai-tts-api .
-sudo docker run -p 8000:8000 --name thai-tts-api thai-tts-api
-Testing by curl 
- Windows:  curl -o male.wav -H "Content-Type: application/json" -d "{\"text\":\"ทดสอบ\",\"voice\":\"male\"}" http://<server-ip>:8000/tts/
- Linux: curl -v -o male.wav -H "Content-Type: application/json" -d '{"text":"ทดสอบ","voice":"male"}' http://<server-ip>:8000/tts/

   
