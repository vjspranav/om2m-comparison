from locust import HttpUser, task, LoadTestShape, constant, events

import json

with open('nodes.json') as f:
    nodes = json.load(f)

with open('nodesdata.json') as f:
    nodesdata = json.load(f)


MAIN_URL = 'http://10.3.1.117:8001/Mobius'

AQNodes = list(nodes['AE-AQ'])
SRNodes = list(nodes['AE-SR'])
EMNodes = list(nodes['AE-EM'])
WMNodes = list(nodes['AE-WM'])
SLNodes = list(nodes['AE-SL'])
CMNodes = list(nodes['AE-CM'])
WNNodes = list(nodes['AE-WN'])
WENodes = list(nodes['AE-WE'])

class StepLoadShape(LoadTestShape):
    max_users = len(AQNodes + SRNodes + CMNodes + EMNodes + SLNodes + WENodes + WMNodes + WNNodes) # Total number of users
    hatch_rate = max_users  # Spawn all users at once

    def tick(self):
        run_time = self.get_run_time()
        if run_time < 7200:  # 7200 seconds = 2 hours
            return (self.max_users, self.hatch_rate)
        else:
            return (0, 0)  # No new users are spawned after 2 hours

# 1 min 3 reqs
class AQUser(HttpUser):
    wait_time = constant(60)
    fixed_count = len(AQNodes)

    def on_start(self):
        self.node = AQNodes.pop()
        self.data = {
            "m2m:cin":{
                'con': nodesdata[self.node]['con'],
                'lbl': nodesdata[self.node]['lbl'],
                'cnf': nodesdata[self.node]['cnf']
            }
        }
        self.url = MAIN_URL + '/AE-AQ/' + self.node + '/Data?rcn=1'
        self.headers = {
            'X-M2M-RI': '12345',
            'X-M2M-Origin': 'SOrigin' + self.node,
            'Content-Type': 'application/json;ty=4'
        }

    @task
    def run_task(self):
        for _ in range(3):
            self.client.post(self.url, headers=self.headers, json=self.data)

# 1 min 1 req     
class SRUser(HttpUser):
    wait_time = constant(60)
    fixed_count = len(SRNodes)

    def on_start(self):
        self.node = SRNodes.pop()
        self.data = {
            "m2m:cin":{
                'con': nodesdata[self.node]['con'],
                'lbl': nodesdata[self.node]['lbl'],
                'cnf': nodesdata[self.node]['cnf']
            }
        }
        self.url = MAIN_URL + '/AE-SR/' + self.node + '/Data?rcn=1'
        self.headers = {
            'X-M2M-RI': '12345',
            'X-M2M-Origin': 'SOrigin' + self.node,
            'Content-Type': 'application/json;ty=4'
        }
            

    @task
    def run_task(self):
        self.client.post(self.url, headers=self.headers, json=self.data)
    
# 1 min 1 req
class EMUser(HttpUser):
    wait_time = constant(60)
    fixed_count = len(EMNodes)

    def on_start(self):
        self.node = EMNodes.pop()
        self.data = {
            "m2m:cin":{
                'con': nodesdata[self.node]['con'],
                'lbl': nodesdata[self.node]['lbl'],
                'cnf': nodesdata[self.node]['cnf']
            }
        }
        self.url = MAIN_URL + '/AE-EM/' + self.node + '/Data?rcn=1'
        self.headers = {
            'X-M2M-RI': '12345',
            'X-M2M-Origin': 'SOrigin' + self.node,
            'Content-Type': 'application/json;ty=4'
        }

    @task
    def run_task(self):
        self.client.post(self.url, headers=self.headers, json=self.data)

# 2 min 1 req (actually 4 hours but 2 min for testing)
class WMUser(HttpUser):
    wait_time = constant(120) # 2 min
    fixed_count = len(WMNodes)

    def on_start(self):
        self.node = WMNodes.pop()
        self.data = {
            "m2m:cin":{
                'con': nodesdata[self.node]['con'],
                'lbl': nodesdata[self.node]['lbl'],
                'cnf': nodesdata[self.node]['cnf']
            }
        }
        self.url = MAIN_URL + '/AE-WM/' + self.node + '/Data?rcn=1'
        self.headers = {
            'X-M2M-RI': '12345',
            'X-M2M-Origin': 'SOrigin' + self.node,
            'Content-Type': 'application/json;ty=4'
        }

    @task
    def run_task(self):
        self.client.post(self.url, headers=self.headers, json=self.data)

# 1 min 1 req
class SLUser(HttpUser):
    wait_time = constant(60)
    fixed_count = len(SLNodes)

    def on_start(self):
        self.node = SLNodes.pop()
        self.data = {
            "m2m:cin":{
                'con': nodesdata[self.node]['con'],
                'lbl': nodesdata[self.node]['lbl'],
                'cnf': nodesdata[self.node]['cnf']
            }
        }
        self.url = MAIN_URL + '/AE-SL/' + self.node + '/Data?rcn=1'
        self.headers = {
            'X-M2M-RI': '12345',
            'X-M2M-Origin': 'SOrigin' + self.node,
            'Content-Type': 'application/json;ty=4'
        }

    @task
    def run_task(self):
        self.client.post(self.url, headers=self.headers, json=self.data)

# 1 min 1 req
class CMUser(HttpUser):
    wait_time = constant(60)
    fixed_count = len(CMNodes)

    def on_start(self):
        self.node = CMNodes.pop()
        self.data = {
            "m2m:cin":{
                'con': nodesdata[self.node]['con'],
                'lbl': nodesdata[self.node]['lbl'],
                'cnf': nodesdata[self.node]['cnf']
            }
        }
        self.url = MAIN_URL + '/AE-CM/' + self.node + '/Data?rcn=1'
        self.headers = {
            'X-M2M-RI': '12345',
            'X-M2M-Origin': 'SOrigin' + self.node,
            'Content-Type': 'application/json;ty=4'
        }

    @task
    def run_task(self):
        self.client.post(self.url, headers=self.headers, json=self.data)
    
# 22 min 1 req
class WNUser(HttpUser):
    wait_time = constant(1320) # 22 min
    fixed_count = len(WNNodes)

    def on_start(self):
        self.node = WNNodes.pop()
        self.data = {
            "m2m:cin":{
                'con': nodesdata[self.node]['con'],
                'lbl': nodesdata[self.node]['lbl'],
                'cnf': nodesdata[self.node]['cnf']
            }
        }
        self.url = MAIN_URL + '/AE-WN/' + self.node + '/Data?rcn=1'
        self.headers = {
            'X-M2M-RI': '12345',
            'X-M2M-Origin': 'SOrigin' + self.node,
            'Content-Type': 'application/json;ty=4'
        }
    
    @task
    def run_task(self):
        self.client.post(self.url, headers=self.headers, json=self.data)

# 10 sec 1 req
class WEUser(HttpUser):
    wait_time = constant(10)
    fixed_count = len(WENodes)

    def on_start(self):
        self.node = WENodes.pop()
        self.data = {
            "m2m:cin":{
                'con': nodesdata[self.node]['con'],
                'lbl': nodesdata[self.node]['lbl'],
                'cnf': nodesdata[self.node]['cnf']
            }
        }
        self.url = MAIN_URL + '/AE-WE/' + self.node + '/Data?rcn=1'
        self.headers = {
            'X-M2M-RI': '12345',
            'X-M2M-Origin': 'SOrigin' + self.node,
            'Content-Type': 'application/json;ty=4'
        }
    
    @task
    def run_task(self):
        self.client.post(self.url, headers=self.headers, json=self.data)