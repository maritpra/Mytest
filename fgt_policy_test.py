#/usr/bin/python3

import requests
import json

# Base URL for the FortiGate API
base_url = "https://10.47.19.141/api/v2/monitor/firewall/policy-lookup"

# Authentication
headers = {
    "Authorization": "Bearer rf4849813GfGk9phd4ky5cxhs5k9ff"
}

# Load test cases from JSON file
with open("test_packets.json", "r") as file:
    test_cases = json.load(file)

# Store results for summary
summary_results = []

# Run tests
for test in test_cases:
    # Prepare parameters for the API call
    params = {
        "sourceip": test["srcip"],
        "sourceport": test["srcport"],
        "dest": test["dstip"],
        "destport": test["dstport"],
        "protocol": test["protocol"],
        "srcintf": test["srcintf"]
    }
    
    try:
        # Make the API call
        response = requests.get(base_url, headers=headers, params=params, verify=False)
        print(f"Test ID {test['testid']}: {json.dumps(test)}")
        if response.status_code == 200:
            response_data = response.json()
            print(f"Response for Test ID {test['testid']}:", response_data)
            
            # Extract policy_id for the summary
            policy_id = response_data.get("results", {}).get("policy_id", "No Match")
            summary_results.append({"testid": test["testid"], "policy_id": policy_id})
        else:
            print(f"Test ID {test['testid']} failed with status code {response.status_code}: {response.text}")
            summary_results.append({"testid": test["testid"], "policy_id": "Error"})
    except Exception as e:
        print(f"An error occurred in Test ID {test['testid']}: {str(e)}")
        summary_results.append({"testid": test["testid"], "policy_id": "Error"})

# Print Summary Results
print("\nSummary Results:")
for result in summary_results:
    print(f"Test ID: {result['testid']}, Policy ID: {result['policy_id']}")