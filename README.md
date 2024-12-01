running the project 
```bash
python3 my-server.py
python3 my-calls.py
```

The goal was to:

- Connect a Flask server on the Codespace VM to my local machine.
- Create a login system that generates web tokens for secure authorization.

## What I Did
1. Set Up Connection

   - Made port 5000 on the Codespace VM public so I could access it from my local computer.
   - Ran the server script (my-server.py) in the Codespace and the client script (my-calls.py) locally.
   - Confirmed the connection by sending a GET request to the server and receiving a response.
2. Implement Web Token System
   - Added login functionality to generate a JSON Web Token (JWT) on the /login endpoint.
   - Sent the token in the Authorization header for POST requests to the /echo endpoint.
   - Tested both valid and invalid tokens to verify that only authorized requests were processed.
## How It Works
   - Server: Hosts endpoints for login and token-based authorization using Flask.
   - Client: Sends HTTP requests to log in, receive a token, and make secure calls with the token.
   - Flow:
      - Login generates a token.
      - Token is used for secure communication.
      - Invalid or missing tokens are rejected.
## What I Submitted
   - GitHub repo link with the code.
   - This report.