import httpx

# Set up the URL for the local server
url = "http://127.0.0.1:5000/"

# Step 1: Test the GET request to the server
response = httpx.get(url)
print(response.status_code)  # Should print the status code of the response (e.g., 200 if successful)
print(response.text)  # Prints the server's response text

# Step 2: Prepare to log in by sending some user data
auth_data = {
    "id": "phillip.bradford@uconn.edu"  # I'm using an email for login here; the server should recognize this
}

# Send a POST request to the /login endpoint
login_response = httpx.post(url + "login", data=auth_data)
print("Login response status:", login_response.status_code)  # Was the login request successful?

# If login worked, proceed to use the token provided
if login_response.status_code == 200:
    # Extract the token from the login response
    token = login_response.json().get('token')
    print(f"Received Token: {token}")  # Debugging to make sure we actually got a token

    # Data to send to the /echo endpoint
    my_data = {
        "text": "Hello Phil!"  # Just testing a basic string message
    }
    
    # Authorization headers with the token
    headers = {
        "Authorization": f"Bearer {token}"  # Server expects "Bearer <token>" format
    }
    
    # Step 3: Send a valid request to the /echo endpoint
    echo_response = httpx.post(url + "echo", data=my_data, headers=headers)
    print("Echo response status:", echo_response.status_code)  # Was the request successful?
    print("Echo response body:", echo_response.json())  # Check what the server sent back
    
    # Step 4: Test with an invalid token
    invalid_headers = {
        "Authorization": "skibbidi!_-"  # Faking a bad token to see how the server reacts
    }
    
    # Attempting the same request but with invalid authorization
    invalid_echo_response = httpx.post(url + "echo", data=my_data, headers=invalid_headers)
    print("Invalid echo response status:", invalid_echo_response.status_code)  # Should fail (e.g., 401)
    print("Invalid echo response body:", invalid_echo_response.json())  # Check the error message

else:
    # If login failed, print an error message and stop
    print("Login failed!")  # Not much else we can do without a valid token!
