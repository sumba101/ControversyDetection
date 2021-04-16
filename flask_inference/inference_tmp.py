import requests
from requests.structures import CaseInsensitiveDict
import json
text = {
    'root': "Hey Everyone",
    'comments': [
        'hello',
        'nice to meet you',
        'sup bro!'
    ]
}
headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"
res = requests.post("https://14045541c589.ngrok.io/predict_status", headers=headers, data=json.dumps(text))
print(res.json())