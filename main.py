import requests
import base64

url = "http://127.0.0.1:8080/api/v1/get-cat"

credentials = "meow:meow67"
# Add .decode('utf-8') at the end here
encoded = base64.b64encode(credentials.encode()).decode('utf-8')

headers = {
    'Authorization': f'Basic {encoded}'
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status() 
    
    data = response.json()
    print("Success! Cat URL:", data['url'])
except requests.exceptions.RequestException as e:
    print(f"Error connecting to local server: {e}")