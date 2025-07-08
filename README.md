copy file to folder such as /tts-api
cd tts-api
sudo docker build -t thai-tts-api .
sudo docker run -p 8000:8000 --name thai-tts-api thai-tts-api
