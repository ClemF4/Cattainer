#"""
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS  # installed flask-cors to handle security conflicts between browsers and the server

app = Flask(__name__)
CORS(app)  # This line adds something to the header telling my browser that this site is safe

app.config['TEMPLATES_AUTO_RELOAD'] = True #this line is for development & tells the browser to auto reload after changes to html

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

