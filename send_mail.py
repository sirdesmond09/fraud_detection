import requests
import datetime
from decouple import config

def send_simple_message(**data):
    trans_time = datetime.datetime.strptime(data.get('TransactionStartTime'),"%Y-%m-%dT%H:%M:%SZ")

    return requests.post(config('URL'), auth=("api", config('KEY')),data={"from": "Fraud Detection App {}".format(config('SAND_BOX')), 
    "to": [config('EMAIL')],
    "subject": "Fradulent Transaction Found", 
    "text": f"""Hello Admin,
We have found a fradulent transaction on your platform. Please respond immediately to transaction with:
Tran-id: {data.get('TransactionId')}
Amount : {data.get('Amount')}
Time : {trans_time}
Status : {data.get('status')}            
            """})
        
        
