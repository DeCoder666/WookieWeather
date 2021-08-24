from flask import Flask, render_template, request, redirect
from database import *
import requests, json, random



current_temperature1 = 0
temperatureText = ""
weather_description = ""
planetType = ""

def updateWeather(cityN):
    global weather_description
    global current_temperature1
    global temperatureText
    global planetType
    global isCityValid
    isCityValid = "true"
    api_key = "37ca858f4c45b49fcb23030819779fe5"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = cityN
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature1 = y["temp"]
        current_pressure = y["pressure"]
        current_humidity = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        current_temperature1 = current_temperature1 - 273
        if current_temperature1 > 50:
            planetType = "Mustafar"
        elif current_temperature1 > 29:
            planetType = "Tatooine"
        elif current_temperature1 > 20:
            planetType = "Alderaan"
        elif current_temperature1 > 10:
            planetType = "Endor"
        else:
            planetType = "Hoth"
    else:
        isCityValid = "false"




    # current_temperature = format(current_temperature1, ".1f") + "°C"
    # temperatureDescription = ["Yikes! It's " + current_temperature + " outside.",
    #  "Gosh! It's " + current_temperature + " outside.",
    #  "What a beautiful day! It's " + current_temperature + " outside.",
    #  "Woah, it's " + current_temperature + " outside."]
    # temperatureText = temperatureDescription[random.randrange(0,3)]
 
# else:
#     print(" City Not Found ")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'changeme'

# TODO: Add all of the routes you want below this line!
@app.route("/register", methods=['GET', 'POST'])
def register():
    return render_template("register.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    addUser(email, password)
    return render_template("login.html")

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        updateWeather("Jerusalem")
        return render_template("index.html", weather_description = weather_description ,current_temperature = current_temperature1, temperatureDescription = temperatureText, planetType = planetType, isCityValid = isCityValid)
    a = request.form['cityName']
    if '/' in a:
        return render_template("index.html", weather_description = weather_description ,current_temperature = current_temperature1, temperatureDescription = temperatureText, planetType = planetType, isCityValid = isCityValid)
    else:
        return redirect(f"/{a}")

@app.route("/<cityName>", methods=['GET', 'POST'])
def city(cityName):
    updateWeather(cityName)
    return render_template("index.html", weather_description = weather_description ,current_temperature = current_temperature1, temperatureDescription = temperatureText, planetType = planetType, cityName = cityName, isCityValid = isCityValid)

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
