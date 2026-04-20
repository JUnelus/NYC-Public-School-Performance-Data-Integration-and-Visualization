"""
Data Acquisition Module
Fetches NYC school demographics and performance data from the NYC Open Data API (Socrata).
Implements pagination to retrieve all records.
"""

import requests
import os
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Base directory: project root (parent of src/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")

DEMOGRAPHICS_ENDPOINT = "https://data.cityofnewyork.us/resource/vquv-pjuh.json"
PERFORMANCE_ENDPOINT = "https://data.cityofnewyork.us/resource/ci36-d7ea.json"

BATCH_SIZE = 1000


def fetch_all_records(api_endpoint: str, params: dict = None) -> list:
    """
    Fetches all records from a Socrata API endpoint using pagination.

    Args:
        api_endpoint: The API URL.
        params: Optional extra query parameters.

    Returns:
        A list of all records.
    """
    all_records = []
    offset = 0
    base_params = params.copy() if params else {}

    while True:
        base_params["$limit"] = BATCH_SIZE
        base_params["$offset"] = offset

        logger.info(f"Fetching records {offset} - {offset + BATCH_SIZE} from {api_endpoint}")
        response = requests.get(api_endpoint, params=base_params, timeout=30)
        response.raise_for_status()

        batch = response.json()
        if not batch:
            break

        all_records.extend(batch)
        logger.info(f"  Retrieved {len(batch)} records (total: {len(all_records)})")

        if len(batch) < BATCH_SIZE:
            break
        offset += BATCH_SIZE

    return all_records


def save_json(data: list, filepath: str) -> None:
    """Save data to a JSON file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    logger.info(f"Saved {len(data)} records to {filepath}")


if __name__ == "__main__":
    logger.info("Starting data acquisition...")

    demographics_data = fetch_all_records(DEMOGRAPHICS_ENDPOINT)
    performance_data = fetch_all_records(PERFORMANCE_ENDPOINT)

    save_json(demographics_data, os.path.join(RAW_DATA_DIR, "school_demographics.json"))
    save_json(performance_data, os.path.join(RAW_DATA_DIR, "school_performance.json"))

    logger.info("Data acquisition complete.")
