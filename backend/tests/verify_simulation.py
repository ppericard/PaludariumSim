import requests
import sys
import time

def verify_agent_count(min_count=100):
    url = "http://127.0.0.1:8000/api/stats"
    try:
        print(f"Connecting to {url}...")
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            count = data.get("agent_count", 0)
            print(f"Agent count: {count}")
            if count >= min_count:
                print("SUCCESS: Agent count is sufficient.")
                return True
            else:
                print(f"FAILURE: Agent count {count} is less than {min_count}.")
                return False
        else:
            print(f"FAILURE: API returned status code {response.status_code}")
            return False
    except Exception as e:
        print(f"FAILURE: Could not connect to API. Error: {e}")
        return False

if __name__ == "__main__":
    if verify_agent_count():
        sys.exit(0)
    else:
        sys.exit(1)
