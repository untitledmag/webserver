import requests
import base64

url = "http://127.0.0.1:8080/api/v1/ip/lookup"

credentials = "GViuroCFjGJnrn0p6AproeuCDGgMDZMSQMV1SRM1yIQhG7JrnT"

encoded = base64.b64encode(credentials.encode()).decode('utf-8')

headers = {
    'Authorization': f'Bearer {encoded}'
}

payload = {
    'ip':'endercloud.in'
}
try:
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status() 
    
    data = response.json()
    print("Success! Response:\n", data)
except requests.exceptions.RequestException as e:
    print(f"Error connecting to local server: {e}")