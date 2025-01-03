import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoint(endpoint, params=None):
    url = f"{BASE_URL}{endpoint}"
    try:
        print(f"\nTesting: {url}")
        if params:
            print(f"Parameters: {params}")
            response = requests.get(url, params=params)
        else:
            response = requests.get(url)
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Response:", json.dumps(response.json(), indent=2))
        else:
            print("Error:", response.text)
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server. Is it running?")
    except Exception as e:
        print(f"Error: {str(e)}")
    print("-" * 50)

# Test all endpoints
def run_tests():
    # 1. Root endpoint
    test_endpoint("/")

    # 2. Books endpoints
    test_endpoint("/books/")
    test_endpoint("/books/", {"author": "Shakespeare"})
    test_endpoint("/books/1")

    # 3. Authors endpoint
    test_endpoint("/authors/")
    
    # 4. Languages endpoint
    test_endpoint("/languages/")
    
    # 5. Subjects endpoint
    test_endpoint("/subjects/")

if __name__ == "__main__":
    run_tests()