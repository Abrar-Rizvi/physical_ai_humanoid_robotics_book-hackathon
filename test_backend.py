import requests
import json

# Test the backend API
def test_backend():
    # Backend server URL
    base_url = "http://127.0.0.1:8001"

    # Test health endpoint
    print("Testing health endpoint...")
    try:
        health_response = requests.get(f"{base_url}/health")
        print(f"Health status: {health_response.status_code}")
        print(f"Health response: {health_response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")

    print("\n" + "="*50 + "\n")

    # Test query endpoint
    print("Testing query endpoint...")
    query_data = {
        "query": "What is the main topic of the book?",
        "context": "This is a book about humanoid robotics and AI development."
    }

    try:
        query_response = requests.post(
            f"{base_url}/query",
            json=query_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Query status: {query_response.status_code}")
        if query_response.status_code == 200:
            response_data = query_response.json()
            print(f"Response: {json.dumps(response_data, indent=2)}")
        else:
            print(f"Query failed with status {query_response.status_code}")
            print(f"Error: {query_response.text}")
    except Exception as e:
        print(f"Query failed: {e}")

if __name__ == "__main__":
    test_backend()