import requests

class Mobius:
    def __init__(self, XM2MRI, url):
        self.XM2MRI = XM2MRI
        self.url = url
    
    def create_AE(self, name, XM2MORIGIN, labels=[], rr=False):
        data = {
            "m2m:ae": {
                "rn": name,
                "api": "0.2.481.2.0001.001.000111",
                "lbl": labels,
                "rr": rr
            }
        }
        headers = {
            'X-M2M-RI': self.XM2MRI,
            'X-M2M-Origin': XM2MORIGIN,
            'Content-Type': 'application/json;ty=2'
        }

        r = requests.post(self.url, headers=headers, json=data)
        return r.status_code, r.text
    
    def create_container(self, name, parent, XM2MORIGIN, labels=[], mni=120):
        # Create Node
        data = {
            "m2m:cnt":{
                "rn": name,
                "lbl": labels,
                "mni": mni
            }
        }
        headers = {
            'X-M2M-RI': self.XM2MRI,
            'X-M2M-Origin': XM2MORIGIN,
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
    
    def create_cin(self, parent, node, con, lbl, cnf, XM2MORIGIN):
        data = {
            "m2m:cin":{
                "con": con,
                "lbl": lbl,
                "cnf": cnf
            }
        }

        headers = {
            'X-M2M-RI': self.XM2MRI,
            'X-M2M-Origin': XM2MORIGIN,
            'Content-Type': 'application/json;ty=4'
        }

        r = requests.post(self.url + '/' + parent + '/' + node + '/Data?rcn=1', headers=headers, json=data)
        return r.status_code, r.text