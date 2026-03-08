from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

#app.config['TEMPLATES_AUTO_RELOAD'] = True #this line is for development & tells the browser to auto reload after changes to html

@app.route("/")
def index():
    return render_template('index.html')

#Have the app route save zones here & def safe_zones(), do all the JSON logic here, saving it to a file ect
@app.route('/saved_zones', methods=['POST'])
def saved_zones():
    zones_data = request.get_json()
    #Make sure that the data is in the correct format 
    if not isinstance(zones_data, list):
        return jsonify({"status": "error, please input zones correctly"}), 400
    #Make sure zones_data contains less than 10 zones
    if len(zones_data) > 10:
            return jsonify({"status": "error, your zone file is too big, reduce the number & size of zones"}), 400
    
    for zone in zones_data:
        #Check if each zone contains a zoneType
        if "zoneType" not in zone:
            return jsonify({"status": "error, please input zones correctly"}), 400
        #Check if each zone containers a coordinates list
        if "coordinates" not in zone:
            return jsonify({"status": "error, please input zones correctly"}), 400
        #Limit the number of points in the .json to defend against DoS attacks
        if len(zone["coordinates"]) > 50:
            return jsonify({"status": "error, please have less points in your zones"}), 400
        #Check if zoneType is either red or amber
        if zone["zoneType"] != "red" and zone["zoneType"] != "amber":
            return jsonify({"status": "error, please input zones correctly"}), 400        

    #Save the zones into a .json file
    with open('saved_zones.json', 'w') as file:
        json.dump(zones_data, file, indent=4)
    return jsonify({"status": "success"}), 200

#Route the flag file here, it creates a new empty file on my system called trigger_snapshot.flag
@app.route('/triggerSnapshot', methods=['POST'])
def trigger_snapshot():
    with open('trigger_snapshot.flag', 'w') as file:
        pass
    return jsonify({"status": "success"}), 200

#Allow any website to use my website in an iframe on their website (necessary for HA)
#This is low risk since this will only be hosted on the LAN
@app.after_request
def add_header(response):
    response.headers['X-Frame-Options'] = 'ALLOWALL'
    return response
    
if __name__ == "__main__":
    app.run()

