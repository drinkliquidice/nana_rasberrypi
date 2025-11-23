import requests
import json

def send_to_website(data):
    with open('data.json') as file:
        link = json.load(file)['website_api_endpoint']
    url = link  # Replace with your actual API endpoint

    with open(data, 'r') as f:
        data = json.load(f)

    try:
        # Send the POST request with JSON data
        response = requests.post(url, json=data)

        # Check the response status code
        if response.status_code == 200:
            print("JSON data sent successfully!")
            print("Response:", response.json())  # If the API returns JSON
        else:
            print(f"Error sending JSON data. Status Code: {response.status_code}")
            print("Response Text:", response.text)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")