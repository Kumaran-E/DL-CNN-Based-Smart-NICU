import time
import max30100
import Adafruit_DHT
import RPi.GPIO as GPIO
import firebase_admin
from firebase_admin import credentials, db

# Replace the following placeholders with your Firebase credentials
firebase_config = {
    "apiKey": "AIzaSyB6v8sPTO1SukVtAnbS8FVyTNoh112udyI",
    "uthDomain": "acc11-96bcf.firebaseapp.com",
    "databaseURL": "https://acc11-96bcf-default-rtdb.firebaseio.com",
    "projectId": "acc11-96bcf",
    "storageBucket": "acc11-96bcf.appspot.com",
    "messagingSenderId": "986909407379",
    "appId": "1:986909407379:web:faab43ce92f673a281f566",
    "measurementId": "G-Z5JRCJLPRZ"
    # Your Firebase configuration
}

cred = credentials.Certificate({
    "type": "service_account",
    "project_id": "acc11-96bcf",
    "private_key_id": "c11a0f19ce45640ca68ec700e2615fe8e71d06f4",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC1HYOJ30SjguZA\nQ/YefqpOL6ENNTXGVb/FhyRXV2DVvI9Ok6ByczfmRLxVeWq/sndWy7YrTUPA4g85\nOIfJd7y2yEAsSV7AObP8acfGYTxVG/4eU8Xr4ls1icmuJp9fvnV8F5xTtu0UThT6\nEHIOEGRw0mwNv8sER3zhO4+TOJMdeeu9YYeZ/A145uvjsdwYfSbBNWZ4pQFelwEt\nV4eoScyvCioudswxv/RQg2KOwxRsQaVrszhUuDLNi3NMobw0rzAaF5Jh5kn0w35d\nVXyh7BQP1LoLWoHbX33qiM96wTIk1kzBhSN+q0GB8hhIZCpVSJcXSZ/CMQpa58w8\nYhhGXiknAgMBAAECggEADyR35O+9JgvsWEnWVVezFspgpWFiLOzqawdmKxnrx12h\nKv6owX457uSm97Z+Yvyhgajn2C2jkTLVTFbE85ExPqRLc+hxJZKC0S2+6Cp6XYXz\nnxwom2osxLMlIOGrHYQnqnJcPZuOWCOXGWPamqvAL2FIa3Xc8W9QqjwilY/QrPwU\nwq1OiEqsXSORnb4s+YRGQ2RkXPOB2IxRcK8Rn2CzuiWi3CF+Y+eksm33NyGVwU75\npdUdHIOI/Ef7psRpXFVQLgn9yroy9aHnI1fgj8y863h8vn+O8TEFNkIX8o6+fY1n\nHnHwiQStBCmH2dG72kDei9FHxy/TrP9HmOyImZ7h4QKBgQD84kcEMrcmn0wGKyR7\nhCsCT8oL9fyDkKt7NsNhguAr54lvN3hYrQcbeVG0TY+Zt4WZupJwrx420a0XSNAw\nWFogBROfUvB5fxF6sO0C7RI4vhUg/kpRFVRkHIMSvSivhtAfRukJ3cnNuEvf1XTq\n/cl2/YNYoPMv7U9qw+jV1bqHrwKBgQC3WNedVjTUi03Fu80iLKqccCyKchgGIjpr\niNqfAhOMJrgIOJrZTg6RSrBHspI4Ii7vR2jXhK4BGcGFKBotC2VEQMT6OEsMTTnP\n2S6DwECj9fQqHtWQ8+TdOcsjtuXcxmVlFYSxnSYReopnwtDU8WyWJe4aYWR3fy4U\nB18eNVvcCQKBgCErPM1cKZGzSzFz7zEUQN/ov0OaXCiVjSh4ImBj3itkDy67Q9m9\nuDTuUL0pfzBWVfu38QU+suPV1LI9JrFwpUGV6OD46/nDpPNGyY+csMsog3T0ZaME\n/TC0XKzUisWbFSlFD8Pvh0yoY6tUQCWibA5jahrx4XPj2IrUb3G8ut6ZAoGAeOg7\nd+QrfqZGqUjJY+n0sKlAliPbN+BGijd7hDRIU7oMzk8Vvou9C48nZICb8CyKqvx6\nZPV4Ef28ImVprZ7ALxxPSXrp8rjSkQB1riiP+A/v7f7bc3WCzWiZT3oDZ23l250v\nHjm1qv0WXIqaUHLM2s80j2z+ZdcWudqKnU8uvpECgYA1ZGBMtZJ56l17KD8ThRjl\nhQt0GashT5iFne+qBlNLLIpJ5hxp7f3FUojlyNhx23skEJ6jjqRSAA2oxogTjC0g\nCzacIfMrA5SMRo1VoSEllZB+1ZxPWmb9byDakMCiWcaBkl0NCDU53uHn0fkF9ul8\n+vvSOnGyVj2Hb2XmC9nc5A==\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-dpyf2@acc11-96bcf.iam.gserviceaccount.com",
    "client_id": "117103685464755002586",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-dpyf2%40acc11-96bcf.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
    
    # Your service account credentials
})

# Initialize Firebase Realtime Database
firebase_admin.initialize_app(cred, {"databaseURL": firebase_config["databaseURL"]})
root_ref = db.reference()

mx30 = max30100.MAX30100()
mx30.enable_spo2()

# DHT11 sensor configuration
DHT_PIN = 17  # GPIO pin where the DHT11 sensor is connected

# Relay configurations
RELAY_PIN_HEATER = 27  # GPIO pin where the heater relay is connected
RELAY_PIN_ALERT = 26   # GPIO pin where the alert relay is connected

# Default temperature value
default_temperature = 32

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN_HEATER, GPIO.OUT)
GPIO.setup(RELAY_PIN_ALERT, GPIO.OUT)

def control_relay_heater(temperature):
    if temperature is not None and  default_temperature is not None and default_temperature>=temperature:
        print(
default_temperature)
        GPIO.output(RELAY_PIN_HEATER, GPIO.LOW)  # Turn ON heater relay
    elif default_temperature <=40:
        GPIO.output(RELAY_PIN_HEATER, GPIO.HIGH)  # Turn OFF heater relay
    #else:
        #GPIO.output(RELAY_PIN_HEATER, GPIO.LOW)  # Turn OFF heater relay

def control_relay_alert(heart_rate):
    if heart_rate < 70:
        GPIO.output(RELAY_PIN_ALERT, GPIO.LOW)  # Turn ON alert relay
    else:
        GPIO.output(RELAY_PIN_ALERT, GPIO.HIGH)  # Turn OFF alert relay

def update_default_temperature(snapshot):
    global default_temperature
    default_temperature = snapshot.val()




while True:
    mx30.read_sensor()

    hb = int(mx30.ir / 100)
    spo2 = int(mx30.red / 100)
    # Attach a listener to the "temp" key in Firebase
    default_temperature = root_ref.child("temp").get()

    if mx30.ir != mx30.buffer_ir:
        print("Pulse:", hb)
        # Append pulse data to Firebase with timestamp as key
        pulse_data = {str(int(time.time())): hb}
        root_ref.child("pulse").update(pulse_data)

        control_relay_alert(hb)

    if mx30.red != mx30.buffer_red:
        print("SPO2:", spo2)
        # Append spo2 data to Firebase with timestamp as key
        spo2_data = {str(int(time.time())): spo2}
        root_ref.child("spo2").update(spo2_data)

    # Read temperature and humidity from DHT11 sensor
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHT_PIN)
    if humidity is not None and temperature is not None:
        print(f"Temperature: {temperature:.2f}°C, Humidity: {humidity:.2f}%")

        # Append temperature and humidity data to Firebase with timestamp as key
        temperature_data = {str(int(time.time())): temperature}
        root_ref.child("temperature").update(temperature_data)

        humidity_data = {str(int(time.time())): humidity}
        root_ref.child("humidity").update(humidity_data)

        control_relay_heater(temperature)
    else:
        print("Failed to read data from DHT11 sensor")

    # Introduce a delay to avoid overwhelming Firebase
    time.sleep(2)

# Cleanup GPIO (Note: This part may not be executed due to the infinite loop)
GPIO.cleanup()
