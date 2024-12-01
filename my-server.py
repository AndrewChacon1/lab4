from flask import Flask, request, jsonify
import jwt
import datetime

# Initialize the Flask app
app = Flask(__name__)

# Secret key used to sign and verify JWTs
SECRET_KEY = 'my_secret_key'

# Function to generate a JWT token for a user
def generate_token(user_id):
    payload = {
        'user_id': user_id,  # Embed the user's ID in the token
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # Token expires in 30 minutes
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')  # Sign the token with our secret key

# Function to verify a JWT token
def verify_token(token):
    try:
        # Decode the token and return the user ID if valid
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        # Token is valid but expired
        return 'Token has expired'
    except jwt.InvalidTokenError:
        # Token is invalid
        return 'Invalid token'

# Route for the root endpoint (basic sanity check)
@app.route("/")
def hello():
    return "Server is running\n"  # Simple response to confirm the server is up

# Route for user login
@app.route("/login", methods=['POST'])
def login():
    auth_data = request.form  # Retrieve form data from the request
    user_id = auth_data.get("id")  # Extract the 'id' field (this represents the user)
    
    if user_id:
        # Generate a token for the user and return it in the response
        token = generate_token(user_id)
        return jsonify({"status": "success", "token": token}), 200
    else:
        # If no user ID is provided, return an error
        return jsonify({"status": "error", "message": "Invalid login"}), 401

# Route for the echo endpoint (requires authentication)
@app.route("/echo", methods=['POST'])
def echo():
    auth_header = request.headers.get("Authorization")  # Get the Authorization header
    
    if auth_header:
        # Extract the token from the header (assumes "Bearer <token>" format)
        token = auth_header.split(" ")[1]
        user_id = verify_token(token)  # Verify the token
        
        if user_id not in ['Invalid token', 'Token has expired']:
            # Token is valid, so proceed with processing the request
            text = request.form.get('text', '')  # Get the 'text' parameter from the request
            return jsonify({"status": "success", "message": f"User {user_id} said: {text}"}), 200
        else:
            # Token is invalid or expired, return an error
            return jsonify({"status": "error", "message": user_id}), 401
    else:
        # No Authorization header provided
        return jsonify({"status": "error", "message": "Authorization token missing"}), 401

# Run the app on localhost at port 5000
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)  # Accessible on the local network
