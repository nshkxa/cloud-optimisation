import requests
import time
import random

for i in range(1000):
    requests.get("http://127.0.0.1:5000/")
    time.sleep(random.uniform(0.01, 0.1))

print("Traffic generation complete.")
