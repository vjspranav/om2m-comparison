import json
import random
import gevent
import time
import math
from locust import HttpUser, task, between, LoadTestShape
from gevent.lock import Semaphore
from locust import events

HEADER = {
    'X-M2M-Origin': 'SOrigin1',
    'X-M2M-RI': '12345',
    'Content-Type': 'application/json;ty=4;charset=utf-8'
}

class StepLoadShape(LoadTestShape):
    step_time = 60
    step_load = 5
    spawn_rate = 10
    time_limit = 7200

    def tick(self):
        run_time = self.get_run_time()

        if run_time > self.time_limit:
            return None

        current_step = math.floor(run_time / self.step_time) + 1
        return (current_step * self.step_load, self.spawn_rate)

max_users = 500
users_waiting = 0
event = gevent.event.Event()
lock = Semaphore()

class MyUser(HttpUser):
    wait_time = between(1, 1)
    nodes_data = None

    def on_start(self):
        self.start_time = time.time()
        self.all_nodes = []

        with open('nodes.json') as f:
            self.nodes_data = json.load(f)

        for node_type, node_names in self.nodes_data.items():
            self.all_nodes.extend(node_names)

    @task
    def increase_users(self):
        global users_waiting
        global event

        with lock:
            users_waiting += 1
            print(f"{users_waiting} users waiting... ({users_waiting}/{max_users})")
            if users_waiting >= self.environment.runner.user_count:
                print("All users are ready!")
                event.set()

        
        event.wait()  # Wait for the event to be cleared before proceeding
        time.sleep(10)

        user_num = self.environment.runner.user_count
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"User {user_num} - Time: {current_time}")

       
        item = random.choice(self.all_nodes)
        node_type = item.split('-')[0]
        url = f"http://10.3.1.117:8001/Mobius/AE-{node_type}/{item}/Data"
        self.client.get(url, headers=HEADER)


        with lock:
            users_waiting -= 1
            if users_waiting == 0:
                event.clear()
    
 

