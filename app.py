#"""
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS  # installed flask-cors to handle security conflicts between browsers and the server

app = Flask(__name__)
CORS(app)  # This line adds something to the header telling my browser that this site is safe

@app.route("/")
def index():
    return render_template('index.html')

#Have the app route save zones here & def safe_zones(), do all the JSON logic here, saving it to a file ect

@app.after_request
def add_header(response):
    response.headers['X-Frame-Options'] = 'ALLOWALL'
    return response

if __name__ == "__main__":
    app.run(debug=True)
#"""

