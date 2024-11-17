from flask import Flask, request
from werkzeug.exceptions import TooManyRequests

app = Flask(__name__)

# A simple dictionary to store the number of requests per IP
request_counts = {}

@app.before_request
def limit_requests():
    ip = request.remote_addr
    if ip in request_counts:
        request_counts[ip] += 1
    else:
        request_counts[ip] = 1

    if request_counts[ip] > 100:  # Allowing only 100 requests per minute
        raise TooManyRequests("Too many requests, please try again later.")

    # Reset count every minute
    if request_counts[ip] == 1:
        from threading import Timer
        Timer(60, lambda: request_counts.pop(ip, None)).start()

@app.route('/')
def index():
    return "Hello, this is your website!"

if __name__ == "__main__":
    app.run(debug=True)
