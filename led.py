import RPi.GPIO as GPIO
from flask import Flask, render_template, request, redirect, url_for, Markup
import os 
import smbus
import time
import os
import json
import urllib2
import datetime


app = Flask(__name__)
GPIO.setmode(GPIO.BCM)

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   17 : {'name' : 'Entrance light', 'state' : GPIO.LOW},
   18 : {'name' : 'Gate light', 'state' : GPIO.LOW},
   22 : {'name' : 'Outdoor light', 'state' : GPIO.LOW},
   23 : {'name' : 'Bathroom light', 'state' : GPIO.LOW},
   24 : {'name' : 'Room light', 'state' : GPIO.LOW},
   25 : {'name' : 'Fan', 'state' : GPIO.LOW}
   }


print "------------------------"
print "----LOADING MODULES-----"
print "------------------------"

# Set each pin as an output and make it low:
for pin in pins:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)

#Exchange
def getExchangeRates():
    rates = []
    response = urllib2.urlopen('http://api.fixer.io/latest')
    data = response.read()
    rdata = json.loads(data, parse_float=float)
 
    rates.append( rdata['rates']['USD'] )
    rates.append( rdata['rates']['GBP'] )
    rates.append( rdata['rates']['HKD'] )
    rates.append( rdata['rates']['AUD'] )
    return rates

# Login form
@app.route('/', methods=[ 'POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'tester':
            error = 'Invalid credentials!'
        else:
            return redirect(url_for('main'))
    return render_template('login.html', error=error)
@app.route('/login')

def home():
    if not session.get('logged_in'):
	 session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route('/exchange')
def index():
    rates = getExchangeRates()
    return render_template('exchange.html',**locals())   

# Meteo page
@app.route("/meteo")
#@login_required
def meteo():
   DEVICE     = 0x5C #device address
   bus = smbus.SMBus(2)  # Rev 2 Pi uses 1
   addr=DEVICE
   degree = unichr(176)
   data = bus.read_i2c_block_data(addr,0x00, 5)
   temp = str(data[2]) + "." + str(data[3]) + degree  +"C"
   hum = str(data[0]) + "." + str(data[1]) + " %"

   dict = {'Temperature:':temp,'Humidity:':hum}
   return render_template('meteo.html', result = dict)

# Main page
@app.route("/lights")
def main():
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)
   templateData = {
      'pins' : pins
      }

   return render_template('main.html', **templateData)


@app.route("/<changePin>/<action>")

def action(changePin, action):
   changePin = int(changePin)
   # Get the device name for the pin being changed:
   deviceName = pins[changePin]['name']
   # If the action part of the URL is "on," execute the code indented below:
   if action == "on":
      # Set the pin high:
      GPIO.output(changePin, GPIO.HIGH)
      # Save the status message to be passed into the template:
      message = deviceName + " turned on."
   if action == "off":
      GPIO.output(changePin, GPIO.LOW)
      message =  deviceName +" turned off." 
   if action == "toggle":
      # Read the pin and set it to whatever it isn't (that is, toggle it):
      GPIO.output(changePin, not GPIO.input(changePin))
      message = deviceName  + "Toggled" +"."

   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'message' : message,
      'pins' : pins
   }

   return render_template('main.html', **templateData)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=80)
    
