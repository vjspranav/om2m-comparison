from locust import HttpUser, task, LoadTestShape, constant, events, between
from gevent.lock import Semaphore
import random
import json
import time
import gevent
import math

with open('nodes.json') as f:
    nodes = json.load(f)

with open('nodesdata.json') as f:
    nodesdata = json.load(f)


all_nodes = []
for node_type, node_names in nodes.items():
    all_nodes.extend(node_names)

MAIN_URL = 'http://10.3.1.117:8001/Mobius'

users_waiting = 0
event = gevent.event.Event()
lock = Semaphore()

class StepLoadShape(LoadTestShape):
    step_time = 10
    step_load =10
    spawn_rate = 10  # Increase users by 10 every 10 seconds
    time_limit = 14400  # 4 hours

    def tick(self):
        run_time = self.get_run_time()

        if run_time > self.time_limit:
            return None

        current_step = math.floor(run_time / self.step_time) + 1
        return (current_step * self.step_load, self.spawn_rate)
    
class MyUser(HttpUser):
    wait_time = between(1, 1)

    @task
    def increase_users(self):
        global users_waiting
        global event

        with lock:
            users_waiting += 1
            print(f"{users_waiting} users waiting... ({users_waiting})")
            # No need to check for user count limit here

        if event.is_set():  # Check if event is set (all users are ready)
            event.wait()  # Wait for the event to be cleared before proceeding

        user_num = self.environment.runner.user_count
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"User {user_num} - Time: {current_time}")

        item = random.choice(all_nodes)
        node_type = item.split('-')[0]
        headers = {
            'X-M2M-RI': '12345',
            'X-M2M-Origin': 'SOrigin' + item,
            'Content-Type': 'application/json;ty=4'
        }

        data = {
            "m2m:cin":{
                'con': nodesdata[item]['con'],
                'lbl': nodesdata[item]['lbl'],
                'cnf': nodesdata[item]['cnf']
            }
        }

        url = MAIN_URL + '/AE-' + node_type + '/' + item + '/Data?rcn=1'
        # url = f"http://10.3.1.117:8200/~/in-cse/in-name/AE-{node_type}/{item}/Data/la"
        # self.client.get(url, headers=headers)
        self.client.post(url, headers=headers, json=data)

        with lock:
            users_waiting -= 1
            if users_waiting == 0:
                event.clear()

