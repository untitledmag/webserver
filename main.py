import requests
url = "http://127.0.0.1:8080/api/v1/get-cat"

try:
    response = requests.get(url)
    # Check if the request was successful
    response.raise_for_status() 
    
    data = response.json()
    print(data)
except requests.exceptions.RequestException as e:
    print(f"Error connecting to local server: {e}")