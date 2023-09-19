import json
import random
import gevent
import time
import math
from locust import HttpUser, task, between, LoadTestShape
from gevent.lock import Semaphore
from locust import events
from datetime import datetime
HEADER = {
    'X-M2M-Origin': 'admin:admin',
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

        # Calculate the remainder when dividing current_step by 6 (to get multiples of 10)
        remainder = current_step % 6

        # Calculate the adjusted current_step
        adjusted_step = current_step + (6 - remainder) if remainder != 0 else current_step

        return (adjusted_step * self.step_load, self.spawn_rate)

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

        # Calculate the time in seconds elapsed since the start of the minute
        seconds_elapsed = datetime.now().second

        # Check if the seconds elapsed matches the desired intervals
        if seconds_elapsed in [0, 10, 20, 30, 40, 50]:
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
            url = f"http://10.3.1.117:8200/~/in-cse/in-name/AE-{node_type}/{item}/Data"

            # Create the payload data for the POST request
            payload = {
                "m2m:cin": {
                    "lbl": [
                        "AE-AQ",
                        "AQ-SN00-00",
                        "V3.0.0",
                        "AE-AQ-V3.0.0"
                    ],
                    "con": "[1692945820, 190.00, 28.37, 66.2]"
                }
            }

            request_time = time.strftime('%Y-%m-%d %H:%M:%S')
            print(f"Sending request at: {request_time}")

            # Send the POST request with the payload
            self.client.post(url, headers=HEADER, json=payload)

            with lock:
                users_waiting -= 1
                if users_waiting == 0:
                    event.clear()

