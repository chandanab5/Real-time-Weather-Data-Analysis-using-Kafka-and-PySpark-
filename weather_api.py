import requests
import json
import time
from kafka import KafkaConsumer,KafkaProducer

lat = "12.97"
lng = "77.59"
'''from_time = "2022-12-11 09:30:00"
to_time = "2022-12-11 11:00:00"'''
path = "/data/2.5/weather?"

api_key = "07025e8ade66762fcbcd33489429bb79"
url = f"https://api.openweathermap.org{path}lat={lat}&lon={lng}&appid={api_key}&units=metric"
api_request = requests.get(url, headers={"x-api-key": api_key,"Content-type": "application/json"})


producer = KafkaProducer(bootstrap_servers='localhost:9092')
#producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
#value_serializer=lambda m: json.dumps(m).encode('ascii')
topic_name = 'weather'
current_weather = []

for i in range(20):
    
	response = requests.get(url)
	data = json.loads(response.text)
	print(data)
	current = data["main"]["temp"]
	current_weather.insert(i,current)
	print(current_weather)
	producer.send(topic_name, bytes(str(current_weather[i]),'utf-8'))
	time.sleep(1)

