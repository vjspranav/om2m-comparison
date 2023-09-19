# from OneM2M.OM2M import OM2M
from locust import HttpUser, task, LoadTestShape, constant, events
import gevent
import json
import json
import random
import gevent
import time
import math
from locust import HttpUser, task, between, LoadTestShape
from gevent.lock import Semaphore
from locust import events


HEADER = {
    'X-M2M-Origin': 'admin:admin',
    'Content-Type': 'application/json;ty=4;charset=utf-8'
}
with open('nodes.json') as f:
    nodes = json.load(f)

with open('nodesdata.json') as f:
    nodesdata = json.load(f)


MAIN_URL = 'http://10.3.1.117:8200/~/in-cse/in-name'


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
            print(f"{users_waiting} users waiting... ({users_waiting})")
            # No need to check for user count limit here

        if event.is_set():  # Check if event is set (all users are ready)
            event.wait()  # Wait for the event to be cleared before proceeding

        user_num = self.environment.runner.user_count
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"User {user_num} - Time: {current_time}")

        item = random.choice(self.all_nodes)
        node_type = item.split('-')[0]
        url = f"http://10.3.1.117:8200/~/in-cse/in-name/AE-{node_type}/{item}/Data/la"
        self.client.get(url, headers=HEADER)

        with lock:
            users_waiting -= 1
            if users_waiting == 0:
                event.clear()

    
 
