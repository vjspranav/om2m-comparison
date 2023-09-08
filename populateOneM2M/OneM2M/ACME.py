import json 
import requests

class ACME:
    def __init__(self, url, rifile, rvi):
        self.url = url
        self.rvi = rvi
        # if file exists read else empty dict
        try:
            with open(rifile, 'r') as f:
                self.ri = json.load(f)
        except:
            self.ri = {}
    
    def create_AE(self, AE, XM2MRI, labels=[], rr=False):
        data = {
            "m2m:ae": {
                "api": "N" + AE,
                "rn": AE,
                "srv": [
                    self.rvi
                ],
                "rr": rr
            }
        }

        headers = {
            'Content-Type': 'application/json;ty=2',
            'Accept': 'application/json',
            'X-M2M-Origin': 'CAdmin' + AE,
            'X-M2M-RI': XM2MRI,
            'X-M2M-RVI': self.rvi
        }

        r = requests.post(self.url + '/in-cse', headers=headers, data = json.dumps(data))
        if r.status_code == 200 or r.status_code == 201 or r.status_code == 409:
            if self.ri.get(AE) is None:
                self.ri[AE] = {}
                self.ri[AE]['ri'] = r.json()['m2m:ae']['ri']
                self.ri[AE]['nodes'] = {}
                with open('ri.json', 'w') as f:
                    json.dump(self.ri, f)
        
        return r.status_code, r.text.encode('utf8')

    def create_container(self, name, parent, XM2MRI):
            data = {
                "m2m:cnt": {
                    "rn": name,
                    "mbs": 10000,
                    "mni": 10,
                }
            }
            headers = {
                'Content-Type': 'application/json;ty=3',
                'Accept': 'application/json',
                'X-M2M-Origin': 'CAdmin' + parent,
                'X-M2M-RI': XM2MRI,
                'X-M2M-RVI': self.rvi
            }

            r = requests.post(self.url + '/' + self.ri[parent]['ri'], headers=headers, data = json.dumps(data))
            if r.status_code == 200 or r.status_code == 201 or r.status_code == 409:
                if self.ri[parent]['nodes'].get(name) is None:
                    self.ri[parent]['nodes'][name] = {}
                    self.ri[parent]['nodes'][name]['ri'] = r.json()['m2m:cnt']['ri']
                    self.ri[parent]['nodes'][name]['nodes'] = {}
                    with open('ri.json', 'w') as f:
                        json.dump(self.ri, f)

            # create Data container
            data = {
                "m2m:cnt": {
                    "rn": "Data",
                    "mbs": 10000,
                    "mni": 10,
                }
            }

            r = requests.post(self.url + '/' + self.ri[parent]['nodes'][name]['ri'], headers=headers, data = json.dumps(data))

            if r.status_code == 200 or r.status_code == 201 or r.status_code == 409:
                if self.ri[parent]['nodes'][name]['nodes'].get('Data') is None:
                    self.ri[parent]['nodes'][name]['nodes']['Data'] = {}
                    self.ri[parent]['nodes'][name]['nodes']['Data']['ri'] = r.json()['m2m:cnt']['ri']
                    with open('ri.json', 'w') as f:
                        json.dump(self.ri, f)
            
            return r.status_code