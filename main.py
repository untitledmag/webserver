import requests
import base64

url = "http://127.0.0.1:8080/api/v1/get-cat"

credentials = "GViuroCFjGJnrn0p6AproeuCDGgMDZMSQMV1SRM1yIQhG7JrnT"
# Add .decode('utf-8') at the end here
encoded = base64.b64encode(credentials.encode()).decode('utf-8')

headers = {
    'Authorization': f'Bearer {encoded}'
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status() 
    
    data = response.json()
    print("Success! Response:\n", data)
except requests.exceptions.RequestException as e:
    print(f"Error connecting to local server: {e}")