import os  
from flask import Flask, redirect, request, send_file
from urllib.parse import unquote
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import re
import logging
# import argparse
# import waitress

app = Flask(__name__)

# logging config
# logging.basicConfig(level=logging.DEBUG)
from logging.config import dictConfig
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})
logger = logging.getLogger(__name__)

# Set your proxy information here
PROXY_HOST = os.environ.get('PROXY_HOST', '')
PROXY_PORT = os.environ.get('PROXY_PORT', '')
PROXY_PORT = int(PROXY_PORT) if PROXY_PORT != '' else 0
PROXY_USERNAME = os.environ.get('PROXY_USERNAME', '')
PROXY_PASSWORD = os.environ.get('PROXY_PASSWORD', '')
PROXIES = {
    'http':  f'socks5://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}',
    'https': f'socks5://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}',
} if (PROXY_HOST != '' and PROXY_PORT != 0) else {}

# Read host and port from environment variables or use defaults
HOST = os.environ.get('HOST', '0.0.0.0')
PORT = os.environ.get('PORT', '5000')
PORT = int(PORT) if PORT != '' else 0


# Define a function to make HTTP requests via the proxy
def get_307(url):
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    # session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    try:
        response = session.get(url, proxies=PROXIES, allow_redirects=False, timeout=5)
        app.logger.info(f"HTTP Request via \"{PROXIES}\" - URL: {url}, Status Code: {response.status_code}")
        # response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        
    except requests.RequestException as e:
        app.logger.error(f"Error making HTTP request - URL: {url}, Error: {e}")
        return f"Failed making request, please try again."

    # Extract the real location from the 307 redirect
    real_location = response.headers['Location']
    real_location = re.sub(r'\?.*', '', real_location)  # Remove the query string
    app.logger.info(f"Resolve Successful - URL: {url}, Result: {real_location}")

    return real_location


# Define a function to validate alphanumeric string
def is_valid_alphanumeric(s):
    # the shared links ever in xhs haven't consumed the capacity of 6-symbol alphanumerics. 
    # Say, it's 62^6 = 56,800,235,584
    # Also, check Miller's Law
    # Limit the length by now, will lift if the xhslink.com pool overflows 6-symbol. 
    if (len(s) > 6):
        return False
    return bool(re.match("^[a-zA-Z0-9]+$", s))


# Serve the frontend
@app.route('/', methods=['GET'])
def handle_index():
    # Extract the client IP from the X-Forwarded-For header or use the remote address
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    # Log the client IP along with other information
    app.logger.info(f"GET /, Client IP: {client_ip}")

    return send_file('index.html')


# Define a route for redirecting
@app.route('/<shortcode>', methods=['GET'])
def handle_shortcode(shortcode):
    # Extract the client IP from the X-Forwarded-For header or use the remote address
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    # Log the client IP along with other information
    app.logger.info(f"GET /{shortcode}, Client IP: {client_ip}")

    if not is_valid_alphanumeric(shortcode):
        app.logger.info(f"Invalid shortcode: {shortcode}")
        return "Invalid shortcode"

    full_url = f'https://xhslink.com/{shortcode}'
    real_location = get_307(full_url)

    return redirect(real_location, code=302)


# Define a route for handling shortcode requests
@app.route('/code/<shortcode>', methods=['GET'])
def resolve_code(shortcode):
    # Extract the client IP from the X-Forwarded-For header or use the remote address
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    # Log the client IP along with other information
    app.logger.info(f"GET /code/{shortcode}, Client IP: {client_ip}")

    if not is_valid_alphanumeric(shortcode):
        app.logger.info(f"Invalid shortcode: {shortcode}")
        return "Invalid shortcode"

    # Construct the full URL
    full_url = f'https://xhslink.com/{shortcode}'
    # Do the same as in the handle_shortcode function
    real_location = get_307(full_url)

    return real_location


# Define a route for handling full url requests
@app.route('/full/', methods=['GET'])
def resolve_full():
    full_url = request.args.get('url', '')

    # Extract the client IP from the X-Forwarded-For header or use the remote address
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    # Log the client IP along with other information
    app.logger.info(f"GET /full/?url={full_url}, Client IP: {client_ip}")

    # Extract the shortcode from the full URL (assuming it follows the pattern xhslink.com/xxxxxx)
    match = re.search(r'xhslink\.com/([a-zA-Z0-9]+)', full_url)

    if match:
        shortcode = match.group(1)
        
        if not is_valid_alphanumeric(shortcode):
            app.logger.info(f"Invalid shortcode: {shortcode}")
            return "Invalid shortcode"
        
        # Make a request to resolve the shortcode
        real_location = get_307(f'https://xhslink.com/{shortcode}')

        return real_location
    
    else: 
        app.logger.info(f"No valid URL found in \"{full_url}\" ")
        return "No valid URL found"

if __name__ == '__main__':
    # Parse command-line arguments
    # parser = argparse.ArgumentParser(description='Run the server for shortcode processing')
    # parser.add_argument('host', type=str, default='0.0.0.0', help='Server address')
    # parser.add_argument('port', type=int, default=5000, help='Port number')
    # args = parser.parse_args()
    # Run the Flask application
    # app.run(host=args.host, port=args.port)
    
    # Run the Flask application
    from waitress import serve
    serve(app, host=HOST, port=PORT)
    

