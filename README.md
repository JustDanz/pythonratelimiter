# Flask DDoS Protection Web Application

This repository contains a simple Flask web application that includes a rate limiting feature to help defend against Distributed Denial of Service (DDoS) attacks.

## Overview
The application uses a dictionary to track the number of requests per IP address. If an IP makes more than 100 requests within a minute, a `TooManyRequests` error is raised to prevent abuse.

### How It Works:
1. **Rate Limiting**:
   - Each IP address is tracked for the number of requests.
   - If an IP exceeds 100 requests within a 60-second window, a `TooManyRequests` exception is raised.
   - After the limit is reached, the request count for the IP address is reset.

## Python Code

```python
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
```

## Features
- **Rate Limiting**: Automatically blocks IP addresses that exceed 100 requests per minute.
- **Protection Against DDoS Attacks**: Filters malicious traffic and prevents potential abuse.

1. **Set Up Environment**:
   - Make sure you have Python 3 installed.
   - Install the required packages:
     ```bash
     pip install Flask werkzeug
     ```

2. **Access the Web Application**:
   - Open your web browser and navigate to `http://localhost:5000/` to see the application in action.

## Contributing
Feel free to fork this repository and make improvements! Contributions like new features, bug fixes, and optimizations are welcome.

---
