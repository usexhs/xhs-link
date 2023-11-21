import os  
from flask import Flask, redirect, request, send_file
from urllib.parse import unquote
import requests
import re
import argparse
import waitress

app = Flask(__name__)


# Set your proxy information here
PROXY_HOST = os.environ.get('PROXY_HOST', '')
PROXY_PORT = int(os.environ.get('PROXY_PORT', ''))
PROXY_USERNAME = os.environ.get('PROXY_USERNAME', '')
PROXY_PASSWORD = os.environ.get('PROXY_PASSWORD', '')
# Read host and port from environment variables or use defaults
HOST = os.environ.get('HOST', '0.0.0.0')
PORT = int(os.environ.get('PORT', '5000'))


# Define a function to make HTTP requests via the proxy
def get_307(url):
    # comment out the proxies if you don't need it
    proxies = {
        'http': f'socks5://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}',
        'https': f'socks5://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}',
    }

    try:
        response = requests.get(url, proxies=proxies, allow_redirects=False)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        
    except requests.RequestException as e:
        print(f"Error making request: {e}")
        return None

    # Extract the real location from the 307 redirect
    real_location = response.headers['Location']
    real_location = re.sub(r'\?.*', '', real_location)  # Remove the query string

    return real_location


# Define a function to validate alphanumeric string
def is_valid_alphanumeric(s):
    return bool(re.match("^[a-zA-Z0-9]+$", s))


# Serve the frontend
@app.route('/', methods=['GET'])
def handle_index():
    return send_file('index.html')


# Define a route for redirecting
@app.route('/<shortlink>', methods=['GET'])
def handle_shortlink(shortlink):
    if not is_valid_alphanumeric(shortlink):
        return "Invalid shortlink format"

    full_url = f'https://xhslink.com/{shortlink}'
    real_location = get_307(full_url)

    return redirect(real_location, code=302)


# Define a route for handling shortcode requests
@app.route('/code/<shortlink>', methods=['GET'])
def resolve_code(shortlink):
    if not is_valid_alphanumeric(shortlink):
        return "Invalid shortlink format"

    # Construct the full shortlink URL
    full_shortlink_url = f'https://xhslink.com/{shortlink}'
    # Do the same as in the handle_shortlink function
    real_location = get_307(full_shortlink_url)

    return real_location


# Define a route for handling full url requests
@app.route('/full/', methods=['GET'])
def resolve_full():
    full_url = request.args.get('url', '')

    # Extract the shortlink from the full URL (assuming it follows the pattern shortlink.com/xxxxxx)
    match = re.search(r'xhslink\.com/([a-zA-Z0-9]+)', full_url)

    if match:
        shortlink = match.group(1)
        # Make a request to resolve the shortlink
        real_location = get_307(f'https://xhslink.com/{shortlink}')

        return real_location


if __name__ == '__main__':
    # Parse command-line arguments
    # parser = argparse.ArgumentParser(description='Run the server for shortlink processing')
    # parser.add_argument('host', type=str, default='0.0.0.0', help='Server address')
    # parser.add_argument('port', type=int, default=5000, help='Port number')
    # args = parser.parse_args()
    # Run the Flask application
    # app.run(host=args.host, port=args.port)
    
    # Run the Flask application
    from waitress import serve
    serve(app, host=HOST, port=PORT)
    

