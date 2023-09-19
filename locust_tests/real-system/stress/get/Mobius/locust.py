import json
import random
import gevent
import time
import math
from locust import HttpUser, task, between, LoadTestShape
from gevent.lock import Semaphore
from locust import events
HEADER = {
    'X-M2M-Origin': 'SOrigin',
    'X-M2M-RI': '12345',
    'Content-Type': 'application/json;ty=4;charset=utf-8'
}

class StepLoadShape(LoadTestShape):
    step_time = 10
    step_load = 10
    spawn_rate = 10  # Increase users by 10 every 10 seconds
    time_limit = 14400  # 4 hours

    def tick(self):
        run_time = self.get_run_time()

        if run_time > self.time_limit:
            return None

        current_step = math.floor(run_time / self.step_time) + 1
        return (current_step * self.step_load, self.spawn_rate)


users_waiting = 0
event = gevent.event.Event()
lock = Semaphore()

with open('nodes.json') as f:
    nodes_data = json.load(f)

class MyUser(HttpUser):
    wait_time = between(1, 15)
    nodes_data = None

    def on_start(self):
        self.start_time = time.time()
        self.all_nodes = []

        for node_type, node_items in nodes_data.items():
            for item in node_items:
                self.all_nodes.append((node_type, item))  # Store both node type and item

    @task
    def increase_users(self):
        global users_waiting
        global event

        with lock:
            users_waiting += 1
            print(f"{users_waiting} users waiting...")
            if users_waiting >= self.environment.runner.user_count:
                print("All users are ready!")
                event.set()

        if event.is_set():  # Check if event is set (all users are ready)
            event.wait()  # Wait for the event to be cleared before proceeding

        user_num = self.environment.runner.user_count
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"User {user_num} - Time: {current_time}")

        node_type, item = random.choice(self.all_nodes)
        url = f"http://10.3.1.117:8001/Mobius/{node_type}/{item}/Data"
        self.client.get(url, headers=HEADER)

        with lock:
            users_waiting -= 1
            if users_waiting == 0:
                event.clear()
