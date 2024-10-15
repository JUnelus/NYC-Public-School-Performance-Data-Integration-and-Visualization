import requests
import os
import json

def get_school_demographics(api_endpoint):
    """Fetches school demographic data from the NYC Open Data API."""
    response = requests.get(api_endpoint)
    response.raise_for_status()  # Raise an exception for bad status codes
    return response.json()

def get_school_performance(api_endpoint):
    """Fetches school performance data from the NYC Open Data API."""
    response = requests.get(api_endpoint)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    demographics_endpoint = "https://data.cityofnewyork.us/resource/vquv-pjuh.json"
    performance_endpoint = "https://data.cityofnewyork.us/resource/ci36-d7ea.json"

    demographics_data = get_school_demographics(demographics_endpoint)
    performance_data = get_school_performance(performance_endpoint)

    # Create the data/raw directory if it doesn't exist
    os.makedirs("data/raw", exist_ok=True)

    # Save the raw data to the data/raw directory as JSON files
    with open("data/raw/school_demographics.json", "w") as f:
        json.dump(demographics_data, f, indent=4)

    with open("data/raw/school_performance.json", "w") as f:
        json.dump(performance_data, f, indent=4)