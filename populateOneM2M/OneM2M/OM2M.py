import requests

class OM2M:
    def __init__(self, username, password, url):
        self.username = username
        self.password = password
        self.url = url
        
    def create_AE(self, name, labels=[], rr=False):
        data = {
            "m2m:ae": {
                "rn": name,
                "lbl": labels,
                "rr": rr,
                "api": name
            }
        }
        headers = {
            'X-M2M-Origin': self.username + ':' + self.password,
            'Content-Type': 'application/json;ty=2'
        }
        r = requests.post(self.url, headers=headers, json=data)
        return r.status_code, r.text
    
    def create_container(self, name, parent, labels=[], mni=120):
        # Create Node
        data = {
            "m2m:cnt":{
                "rn": name,
                "lbl": labels,
                "mni": mni
            }
        }
        headers = {
            'X-M2M-Origin': self.username + ':' + self.password,
            'Content-Type': 'application/json;ty=3'
        }

        r = requests.post(self.url + '/' + parent, headers=headers, json=data)

        # Create Data Container inside Node
        data = {
            "m2m:cnt":{
                "rn": "Data",
                "lbl": labels,
                "mni": mni
            }
        }

        r = requests.post(self.url + '/' + parent + '/' + name, headers=headers, json=data)

        return r.status_code
    
    def create_cin(self, parent, node, con, lbl, cnf):
        data = {
            "m2m:cin":{
                "con": con,
                "lbl": lbl,
                "cnf": cnf
            }
        }
        headers = {
            'X-M2M-Origin': self.username + ':' + self.password,
            'Content-Type': 'application/json;ty=4'
        }
        r = requests.post(self.url + '/' + parent + '/' + node + '/Data', headers=headers, json=data)
        return r